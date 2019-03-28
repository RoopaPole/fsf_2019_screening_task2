# FOSSEE Fellowship 2019 Screening Task 2

# Task Description:

        -Load a csv file using ‘Load’ option available under “File” menu.
        
        -Display the complete data from the loaded csv as a table.
        
        -Edit the existing data in the table using the ‘Edit data’ option under the “Edit” menu.
        
        -Add new data to the table using ‘Add data’ option under “File” menu.
        
        -Select any number of columns from the displayed table.
        
        -Plot the data from any two selected columns should be available as buttons as mentioned below:
        
                     1.Plot scatter points

                     2.Plot scatter points with smooth lines

                     3.Plot lines
           
        -Click on any of the plot button. Plot should be generated accordingly in a new tab.
        
        -Label x-axis and y-axis accordingly.
        
        -Add a title to the graph.
        
        -Save the plot as .png file using ‘Save as png’ option under “File” menu.
        
  # Working of application:
  
   ->CSV file is loaded by clicking on 'Load' option which is there under "File" menu.
   
   -> after loading the csv file it displays the content of CSV file in the form of table.
   
   -> you can edit the data by clicking on 'Edit data' available under "File" menu.
   
   -> you can also add data by using 'Add data' under "File menu".
   
   -> if you want to plot the data you have to select two columns from two comboboxes.
   
         -if you select only column1 or column2 it raises a message box saying like "P lease select columns again!!!" and  if the
         
         columns are same also  it raises a message as x-axis and y-axis should not be same.
      
   ->after selecting two columns you can click on any one of the three buttons which shows plotting between two columns.
   
   and lable x-axis,y-axis are added accordingly to the selected columns and also title is added to the ploted image.
     
   ->3 buttons are:
   
         1.scatter points.
         
         2.scatter points with smooth lines.
         
         3.lines.
  **NOTE: make sure that plotting should be between only numric data, that means you have to select the columns with numeric data.
       
  ->After plotting you can save plotted image as .png by selecting 'SaveasPNG' option under "File" menu.
  
  ->before loading the CSV file if you select 'edit data'  or  'plot data'  or  'SaveasPNG'  or  'AddData'  it shows a message box by 
  
  saying  that "Please load CSV file First!!!".
  
  ->After Laoding the data if you select the option Save as PNG then it raises a messge line "Please Plot First!!!"
