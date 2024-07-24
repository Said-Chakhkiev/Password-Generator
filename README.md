# Password-Generator
Installation
To run the application, you need Python 3.x and the following libraries:
googletrans for text translation.
pandas for data handling, including reading and writing Excel files.
openpyxl for working with Excel files (required by pandas for reading Excel).
python-docx for working with Word files
<pre><code class="sh">
pip install googletrans==4.0.0-rc1
pip install pandas
pip install openpyxl
pip install python-docx
</code></pre>

# Launching the Application:
Run the application by executing the main.py script:
<pre><code class="sh">
  python main.py
</code></pre>

# Uploading a File:
Click the "Browse" button to select a file containing names and surnames. The file should be in .txt, .json, or .xlsx format, where each line contains one name and surname separated by a space.

# Selecting a Translation Language:
Choose the target translation language from the dropdown menu. Available languages are English (en), Spanish (es), French (fr), German (de), and Russian (ru).

# Configuring Password Parameters:
Specify the password length in the "Password length" field.

Select the type of characters for the password from the dropdown menu:
"letters" — only letters.
"letters_digits" — letters and digits.
"all" — letters, digits, and special characters.

# Processing the File:
Click the "Process" button to start processing the file. The application will translate the names and surnames into the selected language and generate passwords with the specified parameters.
Choose a location to save the result. The result will be saved in .txt format, where each line contains the translated name, surname, and password.

Example File
Example content of a file with names and surnames:
<pre><code class="txt">
 Иван Петров
 Анна Сидорова
</code></pre>

Example Result
Example content of the resulting file:
<pre><code class="txt">
 Ivan Petrov Ab123
 Anna Sidorova Cd456
</code></pre>

