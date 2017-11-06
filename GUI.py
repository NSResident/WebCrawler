from Tkinter import *


root = Tk()

def printdepth():
    BF_text = Text(root, height = 7, width = 30)
    BF_text.grid(row = 7, columnspan = 2)
    BF_text.insert(END, "Some \ntext \nlines \nhello \nworld")




url = Label(root, text = "URL")
max_depth = Label(root,text="Max Depth")
max_pages = Label(root, text = "Max Pages")
url_entry = Entry(root)
depth_entry = Entry(root)
pages_entry = Entry(root)
url.grid(row = 0)
max_depth.grid(row = 1)
max_pages.grid(row = 2)
url_entry.grid(row = 0, column = 1)
depth_entry.grid(row = 1, column = 1)
pages_entry.grid(row = 2, column = 1)
subdomains_button = IntVar()
Checkbutton(root, text = "Subdomains", variable = subdomains_button).grid(row = 3, sticky = W)
robots_txt_button = IntVar()
Checkbutton(root, text = "Robots.txt", variable = robots_txt_button).grid(row = 3, column = 1, sticky = W)
dfs_button = IntVar()
Checkbutton(root, text = "DFS", variable = dfs_button).grid(row = 4, sticky = W)
bfs_button = IntVar
Checkbutton(root, text = "BFS",variable = bfs_button).grid(row = 4, column = 1, sticky = W)
crawl_button = Button(root, text = "Crawl", command = printdepth)
crawl_button.grid(row = 5,columnspan = 2, sticky = N+S+E+W)
BF_button = Button(root, text = "BruteForce", command = printdepth)
BF_button.grid(row = 6, columnspan = 2, sticky = N+S+E+W)
#BF_text.grid(row = 6, rowspan = 7, columnspan = 2)
root.mainloop()
