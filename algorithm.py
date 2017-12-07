import os
import time
import pickle
import numpy.random as rd
class Note:
	def __init__(self):
		self.Notebook = None
		self.Title = None
		self.DateCreated = None
		self.UpdatedDate = None
		self.AllUpdates = []
		self.Text = None
		self.References = []
class Data:
	def __init__(self):
		self.Notebooks = []
		self.Notes = []
		
class Security:
	def __init__(self):
		#contains a note and password for it to open and edit
		self.passfornotebooks  = {}

class PyNote:
	def __init__(self):
		print(os.curdir)
		data = os.listdir(os.getcwd()+'/Data')
		#self.masterpath = '/home/nanthan13/workspace/my_projects/PyNote/'
		self.masterpath = os.getcwd()+'/'
		self.Data = Data()
		self.psd = "mastermind"
		self.secured = None
		if 'Data0.pkl' not in data:
			self.Data = Data()
			print("'Data0.pkl' not in data:")
		else:
			print("Loading Data from database")
			files = open(self.masterpath+'Data/Data0.pkl','rb')
			self.Data = pickle.load(files)
			print("File Loaded")
			
	def close(self):
		f1 = open(self.masterpath+'Data/Data0.pkl','wb')
		pickle.dump(self.Data,f1)
		f1.close()
		f = open(self.masterpath+'Data/Temp.txt','w')
		f.close()
		print("Closing PyNote")

	def save(self):
		print("Saving Data")
		f1 = open(self.masterpath+'Data/Data0.pkl','wb')
		pickle.dump(self.Data,f1)
		print("Data Saved")
		f1.close()
		

	def create_note(self):
		directory = self.masterpath+"/Data/Temp.txt"
		notefile = open(directory,'w')
		notefile.write("Notebook:\n"+"Title:\n"+"Date:"+time.ctime()+"\nContent:\n")
		notefile.close()
		os.system("gedit "+directory)
		notefile = open(directory,'r')
		noteobj = Note()
		Notebook1= notefile.readline()
		Text = notefile.read()
		if(Notebook1 !='Notebook:\n'):
			pass
		else:
			while(1):
				os.system("clear")
				book = ""
				try:
					self.notebooks_available()
					book = input("Enter the Notebook to store the notebook:")
				except ValueError:
					continue
				if book not in self.Data.Notebooks:
					self.Data.Notebooks.append(book)
					Notebook1 = book
					break
				elif len(book)>0:
					Notebook1 = book
					break

			notefile.seek(0);notefile.readline();text = notefile.read()
			Text = "Notebook:"+Notebook1+"\n"+text
		noteobj.Notebook= Notebook1
		noteobj.Title = notefile.readline()[6:]
		noteobj.DateCreated  = notefile.readline()[5:]
		if(noteobj.Notebook not in self.Data.Notebooks):
			self.Data.Notebooks.append(noteobj.Notebook)
		notefile.seek(0)
		noteobj.Text = Text
		self.Data.Notes.append(noteobj)
		self.save()

	def notes(self,notebook):
		#returns list of all notes that have same notebook
		listofnotes = []
		if notebook in self.Data.Notebooks:
			for note in self.Data.Notes:
				if note.Notebook == notebook:
					listofnotes.append(note)
			return listofnotes
		else:
			return "Can't find %s"%(notebook)

	def start(self):
		os.system("clear")
		typed_correctly = False
		while(not typed_correctly):
			password = input("Enter the password:")
			if password == self.psd:typed_correctly = True
		ret = 0
		while(ret!=-1):
			ret = self.run()
		self.close()

	def options(self):
		os.system("clear")
		print("WELCOME TO PYNOTE1.0")
		print("STATS:")
		print("      Notebooks:"+str(len(self.Data.Notebooks)))
		print("      Notes    :"+str(len(self.Data.Notes)))
		print("1.Create Note")
		print("2.Edit Note")
		print("3.Delete Note")
		print("4.Delete Notebook")
		print("5.View Notes")
		print("0.exit")
		

	def notebooks(self):
		print("Select the Notebook")
		num = 0
		for Notebook in self.Data.Notebooks:
			print(str(num)+"."+Notebook)
			num+=1
		try:
			sel_num = input("$$$")
		except ValueError:
			print("enter the number")
			sel_num = input("$$$")

		if sel_num.isalpha()==False:
			sel_num = int(sel_num)
			if sel_num < len(self.Data.Notebooks) and sel_num>=0:
				return self.Data.Notebooks[sel_num]
			else:
				return -1
		else:return 'b'


	def notes(self,indices):
		os.system("clear")
		os.system("clear")
		for index in indices:
			if len(self.Data.Notes[index].Text)<400:
				print(str(index)+"."+self.Data.Notes[index].Text)
				print("\n")
			else:
				print(str(index)+"."+self.Data.Notes[index].Text[:401]+"...")
				print("\n")
		try:
			sel_num = input("Type the index No. of the note:")
		except ValueError:
			print("enter the number")
			sel_num = input("$$$")

		if sel_num.isalpha()==False:	
			sel_num = int(sel_num)
			if sel_num in indices:
				return sel_num
			else:
				return -1
		else:return 'b'		

			

	def write_note(self,index):
		filename = open(self.masterpath+"/Data/Temp.txt",'w')
		filename.write(self.Data.Notes[index].Text)
		filename.close()

	def read_note(self,index):
		notefile = open(self.masterpath+"/Data/Temp.txt",'r')
		Notebook= notefile.readline()[9:]
		Title = notefile.readline()[6:]
		DateCreated  = notefile.readline()[5:];notefile.seek(0)
		UpdatedDate = time.ctime()
		self.Data.Notes[index].Title = Title
		self.Data.Notes[index].Notebook = Notebook
		self.Data.Notes[index].UpdatedDate = UpdatedDate
		self.Data.Notes[index].Text = notefile.read()
		self.save()

	def edit_note(self):
		os.system("clear")

		
		b1 = False
		while(b1!=True):
			os.system("clear")
			self_notebook = self.notebooks()
			if self_notebook=='b':
				b1 = True
				break
			if self_notebook!=-1:
				indices = []
				num = 0

				for note in self.Data.Notes:
					if note.Notebook == self_notebook:
						indices.append(num)
					num+=1
				
				b2 = False
				if len(indices)>0:
					while(b2!=True):
						sel_note_num = self.notes(indices)
						if sel_note_num=='b':
							b2 = True
							break
						if sel_note_num!=-1:
							self.write_note(sel_note_num)
							os.system("gedit "+self.masterpath+"Data/Temp.txt")
							self.read_note(sel_note_num)
				else:os.system("clear");print("No Notes in this Notebook");time.sleep(.9)

	def del_note(self):
		os.system("clear")
		
		b1 = False
		while(b1!=True):
			os.system("clear")
			self_notebook = self.notebooks()
			if self_notebook=='b':
				b1 = True
				break
			if self_notebook!=-1:
				indices = []
				num = 0
				for note in self.Data.Notes:
					if note.Notebook == self_notebook:
						indices.append(num)
					num+=1
				os.system("clear")
				b2 = False
				if len(indices)>0:
					while(b2!=True):
						sel_note_num = self.notes(indices)
						if sel_note_num=='b':
							b2 = True
							break
						if sel_note_num!=-1:
							while(True):
								yes = input("Type Yes to delete the note:")
								if yes=='Yes':
									self.delete_note(sel_note_num)
									b2 = True
									break
								elif yes == 'b':
									break
				else:os.system("clear");print("No Notes in this Notebook");time.sleep(.9)

												
	def delete_note(self,num):
		del self.Data.Notes[num]

	def notebooks_available(self):
		print("Notebooks already Existing:")
		for notebook in self.Data.Notebooks:
			print(notebook)
			
	def run(self):
		self.options()
		opt = input("$$$")
		if(opt == '1'):
			
			self.notebooks_available()
			self.create_note()
		elif(opt== '2'):
			self.edit_note()
		elif(opt == '3'):
			self.del_note()
		elif(opt=='4'):
			self.del_notebook()
		elif(opt=='5'):
			self.view_notes()
		elif(opt=='0'):
			return -1
	
	def view_notes(self):
		os.system("clear")
		self.view_notes_options()
		sel_num = int(input("Enter the index"))
		os.system("clear")
		if sel_num == 1:
			#Display all Notes by time order
			Notes = list(self.Data.Notes)
			for note in Notes:
				print(note.Text[0:])
				print("\n")
			
		elif sel_num == 2:
			#Display Notes by Notebook
			i =0
			for Notebook in self.Data.Notebooks:
				print(str(i)+"."+Notebook)
				i+=1
			sel_index = int(input("Enter the index"))
			sel_name = self.Data.Notebooks[sel_index]
			for note in self.Data.Notes:
				if note.Notebook == sel_name:
					print(note.Text)
					print("\n")

		elif sel_num == 3:
			#View all the notes by Notebook order
			i=0
			for Notebook in self.Data.Notebooks:
				print("          "+str(i)+"."+Notebook.upper())
				print("\n")

				for note in self.Data.Notes:
					if note.Notebook == Notebook:
						print(note.Text[8+len(Notebook):])
						print("\n")
				i+=1
			
		back = input("'b' for back:")
	
	def view_notes_options(self):
		print("1.Display all Notes by time order")
		print("2.Display Notes by Notebook")
		print("3.View all the notes by Notebook order")

	def del_notebook(self):
		num = 0
		for Notebook in self.Data.Notebooks:
			print(str(num)+"."+Notebook)
			num+=1
		sel_index = int(input("Enter the Index:"))
		sel_name = self.Data.Notebooks[sel_index]
		if(sel_name in self.Data.Notebooks):
			#deleting all notes in the notebook
			while(1):
				ans = input("Are you sure to delete,say yes")
				if ans == 'Yes':
					break
				if ans == 'No' or ans == 'no':
					return 0
			while(1):
				firstlen = len(self.Data.Notes)
				for i in range(len(self.Data.Notes)):
					if self.Data.Notes[i].Notebook == sel_name:
						del self.Data.Notes[i]
						break
				lastlen = len(self.Data.Notes)
				if(firstlen==lastlen):
					break

			del self.Data.Notebooks[sel_index]
			print("The Notebook %s is Deleted"%(sel_name))

	def spliter(self,text):
		data = []
		while(1):
			for ch in text:
				if ch=='\n':
					splitindex = text.index(ch)
					data.append(text[:splitindex])
					text = text[splitindex+1:]
					continue
			break
		return data[0]

	def __note_view(self,note):
		text = note.Text
		splited_data = self.spliter(text)
		Title = splited_data[1][6:]
		Date = splited_data[2][5:11]
		preview = splited_data[4]
		dots = ""
		if len(splited_data)>5:
			dots = "...."

		format_text = Title.upper()+"\n"+Date+"\n"+preview+dots
		return format_text

	def all_notes_view(self,name):
		#name is the name of  the notebook

		#getting the notes under the notebook name
		os.system("clear")
		indices = []
		for i in range(len(self.Data.Notes)):
			if self.Data.Notes[i].Notebook == name:
				indices.append(i)

		for index in indices:
			#format_text = self.__note_view(self.Data.Notes[index])
			print(str(index)+"."+self.Data.Notes[index].Text)
			print("")

if __name__ == '__main__':
	Evernote = PyNote()
	Evernote.start()
