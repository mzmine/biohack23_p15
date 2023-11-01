/*
 * Click nbfs://nbhost/SystemFileSystem/Templates/Licenses/license-default.txt to change this license
 * Click nbfs://nbhost/SystemFileSystem/Templates/Classes/Class.java to edit this template
 */
package org.mzmine.mslibrary.lipid.validator;

import io.github.mzmine.util.MemoryMapStorage;
import io.github.mzmine.util.spectraldb.entry.DBEntryField;
import io.github.mzmine.util.spectraldb.entry.SpectralLibrary;
import io.github.mzmine.util.spectraldb.parser.AutoLibraryParser;
import io.github.mzmine.util.spectraldb.parser.UnsupportedFormatException;
import java.io.File;
import java.io.IOException;
import java.util.UUID;
import org.lifstools.jgoslin.domain.ElementTable;
import org.lifstools.jgoslin.domain.LipidAdduct;
import org.lifstools.jgoslin.domain.LipidParsingException;
import org.lifstools.jgoslin.parser.LipidParser;
import org.lifstools.jgoslin.parser.SumFormulaParser;

/**
 *
 * @author nilshoffmann
 */
public class MsLibraryReader {

    private final LipidParser lipidParser = new LipidParser();
    private final SumFormulaParser sfp = new SumFormulaParser();

    public void read(File mgfFile) throws IOException, UnsupportedFormatException {
        AutoLibraryParser alp = new AutoLibraryParser(10, (spectralLibraryEntryList, alreadyProcessed) -> {
            spectralLibraryEntryList.forEach((t) -> {
                String name = t.getField(DBEntryField.NAME).map((dbentryname) -> dbentryname.toString()).orElse("NA");
                System.out.println("Processing entry: " + name);
                try {
                    System.out.println("Checking if lipid name is parseable!");
                    LipidAdduct lipidAdduct = lipidParser.parse(name);
                    System.out.println(lipidAdduct.toString());
                    String providedSumFormula = t.getField(DBEntryField.FORMULA).map((formula) -> formula.toString()).orElse("");
                    ElementTable et = sfp.parse(providedSumFormula, sfp.newEventHandler());
                    String calculatedSumFormula = lipidAdduct.getSumFormula();
                    System.out.println("Sum Formulas: DB entry: " + et.getSumFormula() + " calculated: " + calculatedSumFormula);
                    System.out.println("Sum Formulas are equal: " + calculatedSumFormula.equals(et.getSumFormula()));
                    Object pepmass = t.getField(DBEntryField.MOLWEIGHT).orElse(Double.valueOf(0));
                    System.out.println("Molweight: " + pepmass.toString());
                    Object mw = t.getField(DBEntryField.PRECURSOR_MZ).orElse(Double.valueOf(0));
                    System.out.println("Precursor MZ: " + mw.toString());
                    double mwd = ((Double)mw).doubleValue();
                    double calculatedMass = et.getMass().doubleValue();
                    System.out.println("Calculated Precursor MZ: "+calculatedMass);
                    System.out.println("Mass difference: "+(mwd-calculatedMass));
                    double diffMass = Math.abs(mwd-calculatedMass);
                    boolean massOk = diffMass<1.0E-3;
                    System.out.println("Mass difference < 1.0E-3? "+massOk);
                } catch (LipidParsingException e) {
                    System.out.println("Goslin says no!");
                }
            });
        });
        String prefix = "lipid-spec-lib-" + UUID.randomUUID();
        boolean parseSuccess = alp.parse(null, mgfFile, new SpectralLibrary(MemoryMapStorage.create(), prefix, File.createTempFile(prefix, ".slib")));
    }

}
