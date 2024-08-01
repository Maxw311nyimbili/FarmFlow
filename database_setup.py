# database_setup.py
import sqlite3


def create_database():
    conn = sqlite3.connect('farm_management.db')
    cursor = conn.cursor()

    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Crop (
        CropID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Type TEXT NOT NULL,
        GrowthDuration INTEGER NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Plot (
        PlotID INTEGER PRIMARY KEY AUTOINCREMENT,
        Location TEXT NOT NULL,
        Size REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Employee (
        EmployeeID INTEGER PRIMARY KEY AUTOINCREMENT,
        Name TEXT NOT NULL,
        Role TEXT NOT NULL,
        HireDate TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Inventory (
        InventoryID INTEGER PRIMARY KEY AUTOINCREMENT,
        ItemName TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        Type TEXT NOT NULL,
        PurchaseDate TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS FinancialRecord (
        RecordID INTEGER PRIMARY KEY AUTOINCREMENT,
        RecordDate TEXT NOT NULL,
        Income REAL NOT NULL,
        Expenses REAL NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Planting (
        PlantingID INTEGER PRIMARY KEY AUTOINCREMENT,
        CropID INTEGER NOT NULL,
        PlotID INTEGER NOT NULL,
        PlantingDate TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        FOREIGN KEY (CropID) REFERENCES Crop(CropID),
        FOREIGN KEY (PlotID) REFERENCES Plot(PlotID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Harvest (
        HarvestID INTEGER PRIMARY KEY AUTOINCREMENT,
        CropID INTEGER NOT NULL,
        PlotID INTEGER NOT NULL,
        HarvestDate TEXT NOT NULL,
        Quantity INTEGER NOT NULL,
        FOREIGN KEY (CropID) REFERENCES Crop(CropID),
        FOREIGN KEY (PlotID) REFERENCES Plot(PlotID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Task (
        TaskID INTEGER PRIMARY KEY AUTOINCREMENT,
        EmployeeID INTEGER NOT NULL,
        PlotID INTEGER NOT NULL,
        TaskDescription TEXT NOT NULL,
        TaskDate TEXT NOT NULL,
        FOREIGN KEY (EmployeeID) REFERENCES Employee(EmployeeID),
        FOREIGN KEY (PlotID) REFERENCES Plot(PlotID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS InventoryUsage (
        UsageID INTEGER PRIMARY KEY AUTOINCREMENT,
        InventoryID INTEGER NOT NULL,
        UsageDate TEXT NOT NULL,
        QuantityUsed INTEGER NOT NULL,
        FOREIGN KEY (InventoryID) REFERENCES Inventory(InventoryID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS PestControl (
        ControlID INTEGER PRIMARY KEY AUTOINCREMENT,
        PlotID INTEGER NOT NULL,
        ControlMethod TEXT NOT NULL,
        ControlDate TEXT NOT NULL,
        Quantity REAL NOT NULL,
        FOREIGN KEY (PlotID) REFERENCES Plot(PlotID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MonthlyCropProduction (
        ProductionID INTEGER PRIMARY KEY AUTOINCREMENT,
        CropID INTEGER NOT NULL,
        FinancialRecordID INTEGER NOT NULL,
        ProductionMonth TEXT NOT NULL,
        QuantityProduced INTEGER NOT NULL,
        FOREIGN KEY (CropID) REFERENCES Crop(CropID),
        FOREIGN KEY (FinancialRecordID) REFERENCES FinancialRecord(RecordID)
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS MarketInfo (
        MarketInfoID INTEGER PRIMARY KEY AUTOINCREMENT,
        CropID INTEGER NOT NULL,
        MarketDate TEXT NOT NULL,
        PricePerUnit REAL NOT NULL,
        FOREIGN KEY (CropID) REFERENCES Crop(CropID)
    )
    ''')

    # Insert initial data
    insert_data(cursor)

    conn.commit()
    conn.close()


def insert_data(cursor):
    # Insert data into Crop table
    cursor.executemany('''
    INSERT INTO Crop (Name, Type, GrowthDuration) VALUES (?, ?, ?)
    ''', [
        ('Maize', 'Cereal', 120),
        ('Sorghum', 'Cereal', 110),
        ('Cassava', 'Root', 365),
        ('Yam', 'Root', 180),
        ('Beans', 'Legume', 90)
    ])

    # Insert data into Plot table
    cursor.executemany('''
    INSERT INTO Plot (Location, Size) VALUES (?, ?)
    ''', [
        ('Accra', 2.5),
        ('Kumasi', 3.0),
        ('Tamale', 1.5),
        ('Takoradi', 4.0),
        ('Cape Coast', 2.0),
        ('Savannah', 0.5),
        ('Aburi', 5.0)
    ])

    # Insert data into Employee table
    cursor.executemany('''
    INSERT INTO Employee (Name, Role, HireDate) VALUES (?, ?, ?)
    ''', [
        ('Kofi Mensah', 'Farmer', '2021-03-15'),
        ('Ama Asante', 'Supervisor', '2020-11-01'),
        ('Yaw Boateng', 'Technician', '2019-08-25'),
        ('Afia Opoku', 'Field Worker', '2022-06-10'),
        ('Kwame Nkrumah', 'Manager', '2018-01-20'),
        ('Joe Puppy', 'Farmer', '2024-05-20')
    ])

    # Insert data into Inventory table
    cursor.executemany('''
    INSERT INTO Inventory (ItemName, Quantity, Type, PurchaseDate) VALUES (?, ?, ?, ?)
    ''', [
        ('Fertilizer', 100, 'Agricultural Input', '2023-01-10'),
        ('Pesticide', 50, 'Chemical', '2023-02-05'),
        ('Seeds', 200, 'Agricultural Input', '2023-03-12'),
        ('Tools', 30, 'Equipment', '2023-04-18'),
        ('Irrigation Pipes', 15, 'Equipment', '2023-10-22')
    ])

    # Insert data into FinancialRecord table
    cursor.executemany('''
    INSERT INTO FinancialRecord (RecordDate, Income, Expenses) VALUES (?, ?, ?)
    ''', [
        ('2023-01-31', 1500.00, 500.00),
        ('2023-02-28', 2000.00, 800.00),
        ('2023-03-31', 2500.00, 700.00),
        ('2023-04-30', 3000.00, 900.00),
        ('2023-05-31', 3500.00, 1000.00)
    ])

    # Insert data into Planting table
    cursor.executemany('''
    INSERT INTO Planting (CropID, PlotID, PlantingDate, Quantity) VALUES (?, ?, ?, ?)
    ''', [
        (1, 1, '2023-01-01', 100),
        (2, 2, '2023-01-15', 150),
        (3, 3, '2023-02-01', 200),
        (4, 4, '2023-02-15', 250),
        (5, 5, '2023-03-01', 300),
        (1, 2, '2023-03-15', 120),
        (2, 3, '2023-04-01', 130),
        (3, 4, '2023-04-15', 140),
        (4, 5, '2023-05-01', 150),
        (5, 1, '2023-05-15', 160)
    ])

    # Insert data into Harvest table
    cursor.executemany('''
    INSERT INTO Harvest (CropID, PlotID, HarvestDate, Quantity) VALUES (?, ?, ?, ?)
    ''', [
        (1, 1, '2023-04-01', 90),
        (2, 2, '2023-04-15', 140),
        (3, 3, '2023-05-01', 180),
        (4, 4, '2023-05-15', 220),
        (5, 5, '2023-06-01', 270),
        (1, 2, '2023-06-15', 110),
        (2, 3, '2023-07-01', 120),
        (3, 4, '2023-07-15', 130),
        (4, 5, '2023-08-01', 140),
        (5, 1, '2023-08-15', 150)
    ])

    # Insert data into Task table
    cursor.executemany('''
    INSERT INTO Task (EmployeeID, PlotID, TaskDescription, TaskDate) VALUES (?, ?, ?, ?)
    ''', [
        (1, 1, 'Planting Maize', '2023-01-01'),
        (2, 2, 'Watering Sorghum', '2023-01-15'),
        (3, 3, 'Fertilizing Cassava', '2023-02-01'),
        (4, 4, 'Weeding Yam', '2023-02-15'),
        (5, 5, 'Harvesting Beans', '2023-03-01'),
        (1, 2, 'Plowing Field', '2023-03-15'),
        (2, 3, 'Applying Pesticides', '2023-04-01'),
        (3, 4, 'Preparing Soil', '2023-04-15'),
        (4, 5, 'Planting New Crops', '2023-05-01'),
        (5, 1, 'Monitoring Crops', '2023-05-15')
    ])

    # Insert data into InventoryUsage table
    cursor.executemany('''
    INSERT INTO InventoryUsage (InventoryID, UsageDate, QuantityUsed) VALUES (?, ?, ?)
    ''', [
        (1, '2023-01-20', 10),
        (2, '2023-02-10', 5),
        (3, '2023-03-15', 20),
        (4, '2023-04-05', 7),
        (5, '2023-05-10', 12)
    ])

    # Insert data into PestControl table
    cursor.executemany('''
    INSERT INTO PestControl (PlotID, ControlMethod, ControlDate, Quantity) VALUES (?, ?, ?, ?)
    ''', [
        (1, 'Spraying', '2023-01-15', 5.0),
        (2, 'Trapping', '2023-02-10', 3.0),
        (3, 'Natural Predators', '2023-03-05', 2.0),
        (4, 'Chemical', '2023-04-15', 4.0),
        (5, 'Organic', '2023-05-20', 1.5)
    ])

    # Insert data into MonthlyCropProduction table
    cursor.executemany('''
    INSERT INTO MonthlyCropProduction (CropID, FinancialRecordID, ProductionMonth, QuantityProduced) VALUES (?, ?, ?, ?)
    ''', [
        (1, 1, '2023-01', 50),
        (2, 2, '2023-02', 60),
        (3, 3, '2023-03', 70),
        (4, 4, '2023-04', 80),
        (5, 5, '2023-05', 90)
    ])

    # Insert data into MarketInfo table
    cursor.executemany('''
    INSERT INTO MarketInfo (CropID, MarketDate, PricePerUnit) VALUES (?, ?, ?)
    ''', [
        (1, '2023-02-01', 10.00),
        (2, '2023-03-01', 12.00),
        (3, '2023-04-01', 8.00),
        (4, '2023-05-01', 15.00),
        (5, '2023-06-01', 7.00)
    ])
