import tkinter as tk
from tkinter import ttk, messagebox
import os
from trie_implementation import insert_word, print_auto_suggestions, deserialize

#Mofiyable file paths 
NOTES_TITLE_FILE = "notes_titles.txt"
NOTES_FOLDER = "notes_content"
TRIE_FILE = "max_english_trie.json"

#Checks if folder for each title content file exist
if not os.path.exists(NOTES_FOLDER):
    os.makedirs(NOTES_FOLDER)

#Variables to store the current word for autocomplete feature
current_prefix = ""
check_suggestions = False  
lastCursorPosition = "1.0"  
lastSpacePosition = "1.0"  

#Initialize the trie
trie_root = deserialize(TRIE_FILE)

#Local dictionary which tracks word occurrences in latest opening of app (Non-dynamic)
word_occurrences = {}

'''Inserts the suggestion selected in place of the prefix'''
def autocomplete(suggestion):
    
    global current_prefix, check_suggestions, lastCursorPosition
    
    #Get the current cursor position
    currentCursorPosition = note_content_text.index(tk.INSERT)
    
    #Find the start position of current word
    line, col = map(int, currentCursorPosition.split('.'))
    start_pos = f"{line}.{col - len(current_prefix)}"
    
    #Delete the partial word and insert the suggestion
    note_content_text.delete(start_pos, currentCursorPosition)
    note_content_text.insert(start_pos, suggestion + " ")
    
    # Move cursor to end of inserted word
    note_content_text.mark_set(tk.INSERT, f"{line}.{col - len(current_prefix) + len(suggestion) + 1}")
    
    #Reset state of suggestion when autocomplete is done
    check_suggestions = False
    current_prefix = ""
    
    #Clear suggestions
    clear_autocomplete_suggestions()

'''Constantly update the current word when the content is edited i.e. A new letter is typed or backspace'''
def update_current_word(event):
    global current_prefix, check_suggestions, lastCursorPosition, lastSpacePosition
    
    #Don't process if a special key is pressed
    if check_suggestions or event.keysym in ('Delete', 'Return'):
        check_suggestions = False
        return
    
    #Get the current cursor position for beinng able to use suggestions when cursor is moved to a word
    currentCursorPosition = note_content_text.index(tk.INSERT)
    line, _ = map(int, currentCursorPosition.split('.'))
    
    # Get the entire line content up to cursor
    line_content = note_content_text.get(f"{line}.0", currentCursorPosition)
    
    #Find the start of current word
    start_index = max(0, len(line_content) - 1)
    while start_index > 0 and line_content[start_index-1] not in (' ', '\n', '\t'):
        start_index -= 1
    
    #Get the current word
    current_prefix = line_content[start_index:].lower()
    
    #Update the suggestions if we have a prefix being made
    if current_prefix.strip():
        update_autocomplete_suggestions()
    else:
        clear_autocomplete_suggestions()
    
    #Track spacebar being pressed for word completion
    if event.char == ' ':
        lastSpacePosition = currentCursorPosition
        word = line_content[start_index:].strip()
        if word:
            track_and_add_word(word)
    
    #Update the position of last cursor 
    lastCursorPosition = currentCursorPosition

'''Trach the word being formed and check if its a new word out of trie. If not, then add word'''
def track_and_add_word(word):
    
    global trie_root
    word = word.lower()
    
    #Skip word that are already in the trie
    suggestions = print_auto_suggestions(trie_root, word)
    if word in suggestions:
        return
    
    #Incremenet occurence of word in dictionary
    if word in word_occurrences:
        word_occurrences[word] += 1
    else:
        word_occurrences[word] = 1
    
    #Add word to the Trie if occurence reach certain iterations
    if word_occurrences[word] >= 3:
        insert_word(trie_root, word)
        word_occurrences.pop(word)

'''Dynamically update the list of suggestion using current_prefix '''
def update_autocomplete_suggestions():

    global current_prefix
    
    #No suggestions if word does not exist    
    if not current_prefix.strip():
        clear_autocomplete_suggestions()
        return
    
    #Get max 10 suggestions for current prefix
    suggestions = print_auto_suggestions(trie_root, current_prefix)
    suggestions = suggestions[:10] 
    
    # Clear existing suggestion buttons
    clear_autocomplete_suggestions()
    
    # Create new buttons for the suggestions
    for i, suggestion in enumerate(suggestions):
        suggestion_button = tk.Button(suggestions_frame, text=suggestion, command=lambda s=suggestion: autocomplete(s), font=("Arial", 12), relief="flat", bd=1)
        suggestion_button.config(bg="#444444", fg="white")
        
        #Make sure only max 5 buttons show up in grid, and max of 2x5 grid is formed
        suggestion_button.grid(row=0+(i//5), column=i%5, padx=5, pady=5, sticky="ew")
        autocomplete_buttons.append(suggestion_button)

'''clear all the visible suggestions buttons'''
def clear_autocomplete_suggestions():
    
    #Destory every button in the autocomplete buttons list
    for button in autocomplete_buttons:
        button.destroy()
    autocomplete_buttons.clear()

'''Loads the titles for each title in the titles file for access'''
def load_note_titles():
    if os.path.exists(NOTES_TITLE_FILE):
        with open(NOTES_TITLE_FILE, "r") as file:
            return file.read().splitlines()
    return []

'''Save the title title in titles file, and making sure the updated title is on top of titles list'''
def save_note_title(title, old_title=None):

    titles = load_note_titles()
    
    #If youre updating title of an existing file, then remove file with old title name
    if old_title and old_title in titles:
        titles.remove(old_title)
    
    # Add new title at the beginning (newest first)
    titles.insert(0, title)
    
    #Add the latest title updated at first of title list
    with open(NOTES_TITLE_FILE, "w") as file:
        file.write('\n'.join(titles) + '\n')

'''Save the content of title (title and data) in seperate text file'''
def save_note_content(title, content):

    #Add txt file with title to titles folder
    note_file = os.path.join(NOTES_FOLDER, f"{title}.txt")
    with open(note_file, "w") as file:
        
        #Make sure first line is always title and rest are conent
        file.write(title + "\n")
        file.write(content)

'''Load content of a selected title'''
def load_note_content(title):
    
    note_file = os.path.join(NOTES_FOLDER, f"{title}.txt")
    if os.path.exists(note_file):
        with open(note_file, "r") as file:
            lines = file.readlines()
            title = lines[0].strip()  # First line is title
            content = ''.join(lines[1:]).strip()  # Rest is the content
            return title, content
    return None, None

'''Delete a title using its title to find txt file'''
def delete_note(title):

    note_file = os.path.join(NOTES_FOLDER, f"{title}.txt")
    
    #Check if title with that file name exists and delete it
    if os.path.exists(note_file):
        os.remove(note_file)
    
    #Update the list of titles, removing the deleted title's title
    titles = load_note_titles()
    if title in titles:
        titles.remove(title)
        with open(NOTES_TITLE_FILE, "w") as file:
            file.write('\n'.join(titles) + '\n')

'''Dynamically update the listbox with titles of current notees'''
def update_notes_list():
    
    titles = load_note_titles()
    
    #Clear the current list
    notes_listbox.delete(0, tk.END)
    
    #Add the titles from updates titles list
    for title in titles:
        notes_listbox.insert(tk.END, title)

'''View content of the selected title'''
def view_note():

    #Find the title selected by cursor
    selected_note = notes_listbox.curselection()
    
    #Check if selected note is not empty title (which does not exist)
    if selected_note:
        note_title = notes_listbox.get(selected_note)
        title, content = load_note_content(note_title)
        
        #Replace previously displayed title and content with selected title and its respective content
        if title:
            note_title_entry.delete(0, tk.END)
            note_title_entry.insert(tk.END, title)
            note_content_text.delete(1.0, tk.END)
            note_content_text.insert(tk.END, content)

'''Clear the title and content fields to add a new title and content'''
def add_note():
    note_title_entry.delete(0, tk.END)
    note_content_text.delete(1.0, tk.END)

'''Save the current title and its content to directory and notes title text file'''
def save_note():

    global lastSpacePosition
    
    #Get the data from both entry fields
    title = note_title_entry.get().strip()
    content = note_content_text.get("1.0", "end-1c")
    
    #Check if either of the fields is left empty (which is not allowed on a new note)
    if not title or not content:
        messagebox.showerror("Error", "Both title and content are required")
        return
    
    #Get the note info for selected bo, and save in old title for case where title is being updated
    selected_note = notes_listbox.curselection()
    if selected_note:
        old_title = notes_listbox.get(selected_note)
    else:
        old_title = None
    
    #Case 1: Updating existing title with same title
    if old_title is not None and old_title == title:
        #Just update content
        save_note_content(title, content)
    
    #Case 2: Changing title of existing title
    elif old_title is not None and old_title != title:
        #Remove old title and add new one at top
        delete_note(old_title)
        save_note_title(title)  #Adds to top of list
        save_note_content(title, content)
    
    
    # Case 3: Creating new title
    else:
        # Only check for duplicates when creating new titles
        if title in load_note_titles():
            response = messagebox.askyesno("Duplicate Title", f"A title with title '{title}' already exists. Create note anyways?")
            
            #Dont do anything if dont want to create new note anyway with same title
            if not response:
                return
        
        #Update title to the top os list of notes
        save_note_title(title)
        save_note_content(title, content)
    
    #Update UI and reset tracking of cursor
    lastSpacePosition = "1.0"
    update_notes_list()
    
    #Select the saved title in the listbox
    try:
        index = notes_listbox.get(0, tk.END).index(title)
        notes_listbox.selection_clear(0, tk.END)
        notes_listbox.selection_set(index)
        notes_listbox.see(index)
    except ValueError:
        pass
    
    messagebox.showinfo("Success", "Note saved successfully!")

'''Save the notes tile to the tiles file, making sure it is set on top of list'''
def save_note_title(title, old_title=None):

    titles = load_note_titles()
    
    #If this is a title change, remove the old title
    if old_title and old_title in titles:
        titles.remove(old_title)
    
    #Remove duplicate if exists (only for new note)
    if title in titles:
        titles.remove(title)
    
    # Add new title at beginning (newest first)
    titles.insert(0, title)
    
    #Update notes title file with newest order
    with open(NOTES_TITLE_FILE, "w") as file:
        file.write('\n'.join(titles) + '\n')

'''Delete the selected title and its content after double checking'''
def delete_current_note():

    #Find the note selected and ask for confirmation
    selected_note = notes_listbox.curselection()
    if selected_note:
        note_title = notes_listbox.get(selected_note)
        response = messagebox.askyesno(
            title="Confirm Deletion",
            message=f"Are you sure you want to delete the title '{note_title}'?",
            icon="warning")
        
        #If yes is clicked, then note is deleted and notes list is updated
        if response:
            delete_note(note_title)
            update_notes_list()
            add_note() #Does the functionality of clearing note too lol
            messagebox.showinfo("Success", f"Note '{note_title}' deleted.")
    else:
        #For case where no title is selected
        messagebox.showerror("Error", "No title selected to delete.")



# Create main window
root = tk.Tk()
root.title("Suggestive Notes App")
root.geometry("1280x720")
root.configure(bg="#1f1f1f")

#Create a main container frame (will contain left and right container)
main_container = tk.Frame(root, bg="#1f1f1f")
main_container.pack(fill="both", expand=True, padx=10, pady=10)

#Left side container (will contain content frame and suggestion frame)
left_container = tk.Frame(main_container, bg="#1f1f1f")
left_container.pack(side="left", fill="both", expand=True)

#Right side container (will contain command buttons frame and listNotes frame)
right_container = tk.Frame(main_container, bg="#1f1f1f")
right_container.pack(side="right", fill="both")

#Content frame for title editing
content_frame = tk.Frame(left_container, bg="#222222", bd=2, relief="solid")
content_frame.pack(side="top", fill="both", expand=True, padx=5, pady=5)

#Suggestions frame for autocomplete
suggestions_frame = tk.Frame(left_container, bg="#222222", bd=2, relief="solid")
suggestions_frame.pack(side="bottom", fill="x", padx=5, pady=5)

#Make grid for suggestions (5 columns)
for i in range(5):
    suggestions_frame.grid_columnconfigure(i, weight=1)

#Command buttons frame
command_buttons_frame = tk.Frame(right_container, bg="#222222", bd=2, relief="solid")
command_buttons_frame.pack(side="top", fill="x", padx=5, pady=5)

#Add grid weights for button frame for filling out space completely
command_buttons_frame.grid_columnconfigure(0, weight=1)
command_buttons_frame.grid_columnconfigure(1, weight=0)
command_buttons_frame.grid_columnconfigure(2, weight=1)
command_buttons_frame.grid_columnconfigure(3, weight=0)
command_buttons_frame.grid_columnconfigure(4, weight=1)
command_buttons_frame.grid_columnconfigure(5, weight=0)
command_buttons_frame.grid_columnconfigure(6, weight=1)

#Add command buttons with proper spacing
add_button = tk.Button(
    command_buttons_frame, text="Add Note", command=add_note,
    fg="white", bg="#00FF00", font=("Arial", 14), relief="flat"
)
add_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

save_button = tk.Button(
    command_buttons_frame, text="Save Note", command=save_note,
    fg="white", bg="#00FF00", font=("Arial", 14), relief="flat"
)
save_button.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

delete_button = tk.Button(
    command_buttons_frame, text="Delete Note", command=delete_current_note,
    fg="white", bg="red", font=("Arial", 14), relief="flat"
)
delete_button.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

#List titles frame with scrollbar
listNotes_frame = tk.Frame(right_container, bg="#222222", bd=2, relief="solid")
listNotes_frame.pack(side="bottom", fill="both", expand=True, padx=5, pady=5)

scrollbar = ttk.Scrollbar(listNotes_frame)
scrollbar.pack(side="right", fill="y")

notes_listbox = tk.Listbox(
    listNotes_frame, width=30, height=15, bg="#333333", fg="white",
    font=("Arial", 12), yscrollcommand=scrollbar.set
)
notes_listbox.pack(side="left", fill="both", expand=True, padx=10, pady=10)
scrollbar.config(command=notes_listbox.yview)

#Allows the note to be viewed when a title is pressed
notes_listbox.bind('<<ListboxSelect>>', lambda e: view_note())

#Autocomplete suggestion buttons
autocomplete_buttons = []

#Note title and content widgets
note_title_label = tk.Label(
    content_frame, text="Title: ", font=("Arial", 16),
    bg="#222222", fg="white"
)
note_title_label.pack(side="top", padx=10, pady=5, anchor="w")

note_title_entry = tk.Entry(
    content_frame, width=50, font=("Arial", 15),
    bg="#444444", fg="white", bd=2
)
note_title_entry.pack(side="top", fill='x', padx=10, pady=5, anchor='w')

note_Content_label = tk.Label(
    content_frame, text="Content: ", font=("Arial", 16),
    bg="#222222", fg="white"
)
note_Content_label.pack(side="top", padx=10, pady=5, anchor="w")

note_content_text = tk.Text(
    content_frame, width=60, height=15, wrap=tk.WORD,
    font=("Arial", 12), bg="#444444", fg="white", bd=2
)
note_content_text.pack(side="top", fill="both", expand=True, padx=10, pady=10)

#Keep updating current word in both entries, by using key release as trigger for new letter entry
note_title_entry.bind("<KeyRelease>", update_current_word)
note_content_text.bind("<KeyRelease>", update_current_word)

#Initialize the app
update_notes_list()
root.mainloop()