import backend.Query

while True:
    opt = -1
    mat = ""
    amount = 1
    print("======\nIf you want to do a normal Query, enter 1\nFor Query with alternate Recipes, enter 2\nFor exit press 0")
    try:
        opt = int(input("Enter: "))
    except ValueError:
        opt = -1
        continue
        
        print(unclean)
    if (opt == 0):
        break
    elif (opt == 1 or opt == 2):
        mat = input("What Item do you want the recipe of? ")
        assert(all(x.isalpha() or x.isspace() for x in mat))
        try:
            amount = int(input("Amount? "))
        except ValueError:
            print("Not an Integer")
            continue
    else:
        continue
    altRecipes =  []
    if (opt == 2):
        s = input("Enter Alt Recipe Names in this Format: X, Y, Z (No Duplicates): ")
        print()
        s = s.split(",")
        clean_input = []
        for i in s:
            e = i
            assert(all(x.isalpha() or x.isspace() for x in i))
            while e.startswith(" "):
                e = e[1:]
            while e.endswith(" "):
                e = e[:-1]
            clean_input += "alt " + e 
        altRecipes = clean_input
    output = backend.Query.queryAlt(mat, altRecipes)
    output_amount = [(a, amount * b) for (a,b) in output]
    print(output_amount)
