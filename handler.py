import sqlite3

con = sqlite3.connect('sat-db')


with con: 
    
    #create a table containing all the mats 
    con.execute(""" 
        CREATE TABLE if not exists Machines(
            name TEXT UNIQUE NOT NULL,
            BuildingID INTEGER PRIMARY KEY AUTOINCREMENT
        );
    """)
    #create Resources Table
    con.execute("""
        CREATE TABLE if not exists Resources (
            name TEXT NOT NULL UNIQUE,
            BuildingID INTEGER,
            IngredientID INTEGER PRIMARY KEY AUTOINCREMENT,
            FOREIGN KEY(BuildingID) REFERENCES Machines(BuildingID)

        );
    """)
    #create Costs table, containing the type of mats needed, aswell as the amount of mats
    con.execute("DROP TABLE if exists costs;")
    con.execute("""
        CREATE TABLE if not exists costs(
            IngredientID NOT NULL,
            output DOUBLE NOT NULL,
            Mat1 DEFAULT NULL,
            Amount1 DOUBLE DEFAULT NULL,
            Mat2 DEFAULT NULL,
            Amount2 DOUBLE  DEFAULT NULL,
            Mat3 DEFAULT NULL,
            Amount3 DOUBLE DEFAULT NULL,
            Mat4 DEFAULT NULL,
            Amount4 DOUBLE DEFAULT NULL,
            OriginalMatName TEXT NOT NULL,
            
            
            FOREIGN KEY(Mat1) REFERENCES Resources(IngredientID),
            FOREIGN KEY(Mat2) REFERENCES Resources(IngredientID),
            FOREIGN KEY(Mat3) REFERENCES Resources(IngredientID),
            FOREIGN KEY(Mat4) REFERENCES Resources(IngredientID),
            FOREIGN KEY(IngredientID) REFERENCES Resources(IngredientID),
            CHECK(((Mat1 NOT NULL AND IFNULL(Amount1,0)) OR (Mat1 IS NULL AND Amount1 IS NULL )) AND
            ((Mat2 IS NOT NULL AND IFNULL(Amount2,0)) OR (Mat2 IS NULL AND Amount2 IS NULL )) AND
            ((Mat3 IS NOT NULL AND IFNULL(Amount3,0)) OR (Mat3 IS NULL AND Amount3 IS NULL )) AND
            ((Mat4 IS NOT NULL AND IFNULL(Amount4,0)) OR (Mat4 IS NULL AND Amount4 IS NULL )))
        );
    """)
    command = """
        INSERT INTO Machines(name)
            SELECT '?'
            WHERE NOT EXISTS ( SELECT * FROM Machines
                                    WHERE name = '?')
    """
    args = ['Constructor','Assembler','Manufacturer','Packager','Refinery', 'Blender', 'Particle_Accelarator', 'Smelter', 'Foundry']
    args = [(el,el) for el in args]
    print(args)
    con.execute("""
        INSERT INTO Machines(name, BuildingID)
            SELECT 'Base', 0
            WHERE NOT EXISTS ( SELECT * FROM Machines
                                    WHERE name = 'Base')
    """)
    con.executemany('INSERT INTO Machines(name) SELECT ?  WHERE NOT EXISTS ( SELECT * FROM Machines WHERE name = ?);', args)
    s = con.execute("""
        SELECT * FROM Machines
    """).fetchall()
    
    print(s)    


