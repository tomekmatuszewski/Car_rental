## Car Rental

Simple command line application 
to manage Car rental database

Libraries used:

     - SQLAlchemy
     - Pytest
     - Typer
     - Black
     - PrettyTable
     
// to run application

    $ python app.py
    
// to get help

    $ python app.py --help
    
    
// to show table

    $ python app.py show-table "table_name"
    
// to search in table

    $ python app.py search-in-table "table_name" "column" "value to search"
    
// to delete row in table

    $ python app.py delete-row "table_name" "number of row to delete"

// to update table

    $ python app.py update-table "table_name" "now number" "column" "new value"
    
// to insert row - row will be inserted at the end of table

    $ python app.py insert-row "table_name" "all datas divided by comma" 