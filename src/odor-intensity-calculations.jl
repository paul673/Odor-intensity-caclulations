module odor

    using GCIdentifier
    using Clapeyron
    using CSV
    using DataFrames

    function get_mixture_activity_coeff(smiles_vector::Array,composition_vector::Array)
        🎅 = []
        for 🎄 in smiles_vector
            push!(🎅 , get_groups_from_smiles(🎄, UNIFACGroups))
        end
        ⭐ = UNIFAC(🎅; puremodel=BasicIdeal)
        return activity_coefficient(⭐, 1.0, 298.15, composition_vector)
    end

    export get_mixture_activity_coeff

    df = DataFrame(CSV.File("src/smiles_pine.csv"))

    basic_smiles = String.(df.basic_smiles)
    smiles = String.(df.smiles)
    new_smiles = []
    new_comp = []
    for i in eachindex(smiles)
        println(smiles[i])
       if smiles[i] in ["C[C@@]12CC[C@@H]3[C@H](CC3(C)C)C(=C)CC[C@H]1O2", "CC1=C[C@H]2[C@@H](CCC(=C2CC1)C)C(C)C",r"C/C/1=C\CCC(=C)[C@H]2CC([C@@H]2CC1)(C)C"]
           println("stop")
       else
           push!(new_smiles, smiles[i])
           push!(new_comp,df.composition[i])
       end
    end

    #new_smiles
    println(get_mixture_activity_coeff(new_smiles ,new_comp))

    #get_mixture_activity_coeff(["CCC"] ,[1])

end # module odor
