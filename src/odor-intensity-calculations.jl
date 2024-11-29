module odor

    using GCIdentifier
    using Clapeyron
    using CSV
    using DataFrames

    function get_mixture_activity_coeff(smiles_vector::Array,composition_vector::Array)
        🎅 = []
        for 🎄 in smiles_vector
            if 🎄=="C=C1CCC2OC2(C)CCC2C1CC2(C)C"
                push!(🎅 , ("C=C1CCC2OC2(C)CCC2C1CC2(C)C", ["CH3" => 3, "CY-CH2" => 5, "CY-CH" => 3, "CY-C" => 2,"CH2=C" => 1,"CH2O" => 1]))
            elseif 🎄=="CC12CCC(CC1)C(C)(C)O2"
                push!(🎅 , ("CC1(C2CCC(O1)(CC2)C)C", ["CH3" => 3, "CY-CH2" => 4, "CY-CH" => 1, "CY-C" => 1, "CH2O" => 1]))#("CC12CCC(CC1)C(C)(C)O2", ["CH3" => 3, "CY-CH2" => 4, "CY-CH" => 1, "CY-C" => 2]))
            else
                push!(🎅 , get_groups_from_smiles(🎄, UNIFACGroups))
            end
        end
        ⭐ = UNIFAC(🎅; puremodel=BasicIdeal)
        return activity_coefficient(⭐, 1.0, 298.15, composition_vector)
    end

    function get_pine_mixture_activity_coeff()
        df = DataFrame(CSV.File("src/smiles_pine.csv"))
        basic_smiles = String.(df.basic_smiles)
        smiles = String.(df.smiles)
        activity_coeff =  get_mixture_activity_coeff(basic_smiles ,Float64.(df.composition))
        df[!,:activity_coeff] = activity_coeff
        CSV.write("src/activity_coeff.csv", df)
        return df
    end

    export get_mixture_activity_coeff
    export get_pine_mixture_activity_coeff


end # module odor
