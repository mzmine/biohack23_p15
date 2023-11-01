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
import org.lifstools.jgoslin.domain.LipidParsingException;
import org.lifstools.jgoslin.parser.LipidParser;

/**
 *
 * @author nilshoffmann
 */
public class MsLibraryReader {
    
    private final LipidParser lipidParser = new LipidParser();

    public void read(File mgfFile) throws IOException, UnsupportedFormatException {
        AutoLibraryParser alp = new AutoLibraryParser(10, (spectralLibraryEntryList, alreadyProcessed) -> {
            spectralLibraryEntryList.forEach((t) -> {
                String name = t.getField(DBEntryField.NAME).orElse("NA");
                System.out.println("Processing entry: " + name);
                try {
                    lipidParser.parse(name);
                } catch (LipidParsingException e) {
                    System.out.println("");
                }
            });
        });
        String prefix = "lipid-spec-lib-" + UUID.randomUUID();
        boolean parseSuccess = alp.parse(null, mgfFile, new SpectralLibrary(MemoryMapStorage.create(), prefix, File.createTempFile(prefix, ".slib")));
    }

}
