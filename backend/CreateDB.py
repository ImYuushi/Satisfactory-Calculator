import re
import os
import sqlite3


def cleanData(data):
    file = open(data, "r")
    raw_data = file.read()
    raw_data = re.sub('>', '>\n', raw_data)
    raw_data = re.sub('<td style="position:relative;overflow:hidden;overflow:clip">', '===', raw_data)
    non_html = re.sub('<.*?>',"  ", raw_data)
    non_html = re.sub('&#160;', '', non_html)
    non_html = re.sub("FICS⁕MAS", "", non_html)
    non_html = re.sub("Recipe Name |Crafting Time \(sec\)  |Ingredients |Products ", '', non_html)
    no_emptylines= [lines for lines in non_html.split("\n") if lines.strip() != ""]
    no_emptylines.pop(0)
    new_data = ""
    for lines in no_emptylines:

        new_data += lines + "\n"
    new_data = re.sub('alt.*?\n', 'alt', new_data)
    #print(new_data)
    return new_data

def formatData(txt):

    #format: [(Matname(str), output/min(double)), [(mat,input/min)]]



    data = cleanData(txt)
    data_list = data.split('===')
    

    formatted = [] 
    #every list element now is one material with its corresponding costs
    #list containing no empty elements
    
    for line in data_list:
        #print(line)
        els = line.split('\n')
        els = [line for line in els if line != '']
        #print(els)
        #print(len(els))
        assert (len(els) - 2) % 3 == 0, ("list not of good length: \n") 
        #print((els[0],els[-2]))
        OriginalMatID = els[-2]
        name = els.pop(0)[:-2]
        #remove crafting time
        els.pop(0)
        amount = els.pop(-1) # output/min
        amount = float(amount.replace('/min ', ''))
        els.pop(-1) #remove output mat (equal to name if it isnt an alt recipe)
        els.pop(-1) #remove output per craft
        #now we have only pairs of amount per craft, mat, mat/min
        #amount per craft can be ignored, not important for us
        mats = []
        #print(els)
        while (len(els) > 0):
            els.pop(0)
            mat = els.pop(0)
            mat = mat[:-2]
            amnt_unf = els.pop(0)
            amnt_f = amnt_unf.replace('/min', '')
            #print(amnt_f)
            mats.append((mat,float(amnt_f)))
        #print(mats)
        formatted.append((name,amount,OriginalMatID, mats))
    return formatted
    #print(formatted)

def lookup(name):
    con = sqlite3.connect('sat-db')
    with con:
        tmp = con.execute("SELECT IngredientID FROM Resources WHERE name = ?;", (name,)).fetchone()
        assert(tmp is not None), name
        #print(tmp)
        return tmp
        
def main():
    constr_form = formatData("Raw_data/constructor_raw.txt")        #1
    assembler_form = formatData("Raw_data/assembler_raw.txt")       #2
    manufacturer_form = formatData("Raw_data/manufacturer_raw.txt") #3
    packager_form = formatData("Raw_data/packager_raw.txt")         #4
    refinery_form = formatData("Raw_data/refinery_raw.txt")         #5
    blender_form = formatData("Raw_data/blender_raw.txt")           #6    
    pa_form = formatData("Raw_data/pa_raw.txt")                     #7      
    smelter_form = formatData("Raw_data/smelter_raw.txt")           #8
    foundry_form = formatData("Raw_data/foundry_raw.txt")           #9
    
    #add to database: 
    """
    step1:  machine wise add all elements to resource table
    step2:  fill cost table
    """
    #print(constr_form)
    con = sqlite3.connect('sat-db')
    #fill resources table
    comb = constr_form + assembler_form + manufacturer_form + packager_form + refinery_form + blender_form + pa_form + smelter_form + foundry_form

    with con:
        for line in constr_form:
            arg = (line[0],line[0])

            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 1 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in assembler_form:
            arg = (line[0],line[0])

            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 2 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in manufacturer_form:
            arg = (line[0],line[0])

            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 3 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in packager_form:
            arg = (line[0],line[0])
            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 4 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in refinery_form:
            arg = (line[0],line[0])
            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 5 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in blender_form:
            arg = (line[0],line[0])
            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 6 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in pa_form:
            arg = (line[0],line[0])
            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 7 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in smelter_form:
            arg = (line[0],line[0])
            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 8 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in foundry_form:
            #print(line[0])
            arg = (line[0],line[0])
            con.execute("""
                INSERT INTO Resources(name, BuildingId)
                SELECT ?, 9 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
            """, arg)
        for line in comb:
            #print(line[3])
            for l in line[3]:
                
                arg = l[0]
                #print(arg)
                con.execute("""
                    INSERT INTO Resources(name, BuildingId)
                    SELECT ?, 0 WHERE NOT EXISTS (SELECT * FROM Resources WHERE name = ?)
                """, (arg,arg))
        #add ingredients to resources

    #fill costs table
    with con: 

        for line in comb:
            #print(line[0])
            mainmat = line[0]
            output = line[1]
            mats = line[3]
            #print(line)
            OriginalMatName = line[2]
            while OriginalMatName.endswith(" "):
                OriginalMatName = OriginalMatName[:-1]
            mats = [(lookup(m),i) for (m,i) in mats]
            l = len(mats)
            command = ''
            id_main = lookup(mainmat)
            #convert mats to big tuple, so it can be fed to execute
            mats_tuple = ()
            for ((a,),b) in mats:
                mats_tuple += (a,b)
            args = (id_main) + (output,) + (OriginalMatName,) + mats_tuple + (id_main)
           # print( args)
            if l == 1:
                con.execute("""INSERT INTO costs(IngredientID, output, OriginalMatName, Mat1, Amount1)
                                SELECT ?, ?, ?, ?, ?  WHERE NOT EXISTS (SELECT * FROM costs WHERE IngredientID = ?);
                """, args)
            if l == 2:
                con.execute("""INSERT INTO costs(IngredientID, output, OriginalMatName, Mat1, Amount1, Mat2, Amount2)
                                SELECT ?, ?, ?, ?, ?, ?, ?  WHERE NOT EXISTS (SELECT * FROM costs WHERE IngredientID = ?);
                """, args)
            if l == 3:
                con.execute("""INSERT INTO costs(IngredientID, output, OriginalMatName, Mat1, Amount1, Mat2, Amount2,Mat3, Amount3)
                                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?  WHERE NOT EXISTS (SELECT * FROM costs WHERE IngredientID = ?);
                """, args)
            if l == 4:
                con.execute("""INSERT INTO costs(IngredientID, output, OriginalMatName, Mat1, Amount1, Mat2, Amount2, Mat3, Amount3, Mat4, Amount4)
                                SELECT ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?  WHERE NOT EXISTS (SELECT * FROM costs WHERE IngredientID = ?);
                """, args)
            
            #print(args)
           


    #print(con.execute("SELECT * FROM costs LIMIT 1").fetchall())
    #print(con.execute("SELECT IngredientId FROM Resources").fetchall())
    #print(con.execute("SELECT * FROM Machines").fetchall())

main()
