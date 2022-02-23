import sqlite3

def lookup(name):
    con = sqlite3.connect('sat-db')
    with con:
        tmp = con.execute("SELECT IngredientID FROM Resources WHERE name = ?;", (name,)).fetchone()
        assert(tmp is not None), (name,)

        return tmp

def rev_lookup(n):
    con = sqlite3.connect('sat-db')
    with con:
        tmp = con.execute("SELECT name FROM Resources WHERE IngredientID = ?;", (n,)).fetchone()
        assert(tmp is not None), n

        return tmp
def convert(l): #convert list of mats and costs to a list of 2-tuples 
    assert len(l) % 2 == 0, 'oops, mistake in query'
    tmp = l 
    ret = []
    while len(tmp) > 0:
        a = tmp.pop(0)
        b = tmp.pop(0)
        ret += [(a,b)]

    return ret



def query(q):
    id = lookup(q)
    

    con = sqlite3.connect('sat-db')
    counter = 0
    with con:
        tmp = con.execute("SELECT * FROM costs WHERE IngredientID = ?", id).fetchone()

        factor = 1
        resources = []
        #remove non mats
        stack = [(id,factor)]
        while len(stack) > 0:
            (a,) = id

            counter += 1
            assert counter < 1000
            tmp = con.execute("SELECT IngredientID, output, OriginalMatName, Mat1, Amount1, Mat2, Amount2, Mat3, Amount3, Mat4, Amount4 FROM costs WHERE IngredientID = ?", id).fetchone()


            #TODO: CHeck this math after sleeping


            #-1 to remove OriginalMatID

            tmp = [l for l in tmp[3:] if l is not None]

            tuples = convert(tmp)

            ingredients_id = [(a,) for (a,b) in tuples]
            ret = []
            non_base_ingredients = []
            for i in ingredients_id:
                tmp = con.execute("""
                    SELECT IngredientID FROM Resources WHERE BuildingID <> 0 AND IngredientID = ?
                """, i)

                non_base_ingredients += tmp.fetchall()

            new_tmp = []
            for i in non_base_ingredients:
                tmp1 = con.execute("SELECT output FROM costs WHERE IngredientID = ?", i).fetchone()
                for (a,b) in tuples:
                    if (a,) == i:
                        factor_n = factor * (b / tmp1[0])
                        new_tmp += [(i, factor_n)]
                        ret += [(a,b,factor_n)]
                        

            stack = new_tmp + stack
            resources += ret
            (id, factor) = stack.pop(0)
        debug = [(a,c) for (a,b,c) in resources]
        res = []
        for (a,c) in debug:
            b = 0
            for (u,v) in res:

                if u - a == 0:
                    b = 1
                    res.remove((u,v))
                    res += [(u,v+c)]
                    break

                    
            if not b:
                res += [(a,c)]

        res = [rev_lookup(a) + (b,) for (a,b) in res]

        return res
            
def queryAlt(q, altList):
    id = lookup(q)
    
    #convert altlist (string list) to id list

    altList = [lookup(i) for i  in altList]

    con = sqlite3.connect('sat-db')
    counter = 0
    with con:
        #make a tuple (altId,OriginalMatID) list
        idList = []
        for i in altList:
            tmp= con.execute("SELECT OriginalMatName FROM costs WHERE IngredientID = ?", i).fetchone()
            (sub,) = tmp 
            tmp = lookup(sub)
            u = i + tmp 
            idList += [u]

        tmp = con.execute("SELECT * FROM costs WHERE IngredientID = ?", id).fetchone()
        factor = 1
        resources = []
        #remove non mats

        for (a,b) in idList:
            if id == b:
                id = a 
                continue
        
        stack = [(id,factor)]
        while len(stack) > 0:

            counter += 1
            assert counter < 1000
            tmp = con.execute("SELECT IngredientID, output, OriginalMatName, Mat1, Amount1, Mat2, Amount2, Mat3, Amount3, Mat4, Amount4 FROM costs WHERE IngredientID = ?", id).fetchone()



            tmp = [l for l in tmp[3:] if l is not None] #correct for OriginalMatID
            #list of tuples containing (prod cost and mat id)
            tuples = convert(tmp)
            #replace ids in tuples with alt id
            tmp_tuples = []


            for (a,b) in tuples:
                guard = 0
                for (u,v) in idList:
                    
                    if (v == a):
                        tmp_tuples += [(u,b)]
                        guard = 1
                        continue
                if guard == 0:
                    tmp_tuples += [(a,b)]

            tuples = tmp_tuples

            ingredients_id = [(a,) for (a,b) in tuples]
            ret = []
            non_base_ingredients = []
            for i in ingredients_id:
                tmp = con.execute("""
                    SELECT IngredientID FROM Resources WHERE BuildingID <> 0 AND IngredientID = ?
                """, i)

                non_base_ingredients += tmp.fetchall()

            new_tmp = []
            for i in non_base_ingredients:
                tmp1 = con.execute("SELECT output FROM costs WHERE IngredientID = ?", i).fetchone()
                for (a,b) in tuples:
                    if (a,) == i:
                        factor_n = factor * (b / tmp1[0])
                        new_tmp += [(i, factor_n)]
                        ret += [(a,b,factor_n)]
                        

            stack = new_tmp + stack
            resources += ret
            (id, factor) = stack.pop(0)
        debug = [(a,c) for (a,b,c) in resources]
        res = []
        for (a,c) in debug:
            b = 0
            for (u,v) in res:

                if u - a == 0:
                    b = 1
                    res.remove((u,v))
                    res += [(u,v+c)]
                    break

                    
            if not b:
                res += [(a,c)]

        res = [rev_lookup(a) + (b,) for (a,b) in res]
        
        return res





""" con = sqlite3.connect('sat-db')
print(con.execute("SELECT * FROM Resources WHERE name = 'Steel Ingot'").fetchall())
    
#query("Reinforced Iron Plate")
r = queryAlt("Reinforced Iron Plate", ["alt Steel Screw"])
print(r) """