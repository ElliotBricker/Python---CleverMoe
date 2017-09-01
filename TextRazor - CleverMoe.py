from Tkinter import *
from PIL import Image, ImageTk
import textrazor

class Application(Frame):
    """"  A GUI application using a class (OO)   """

    def __init__(self, master):
        """    Initialize the Frame  """
        Frame.__init__(self,master)
        self.grid()    # make sure there is a open and close paren here
       
        self.configure(bg="#3355CC")
       
        self.create_widgets()

    def create_widgets(self):
        """  create widgets    """
         
        
        self.path = "E:\CleverMoe\CleverMoeLogo.gif"

        #Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
        self.img = ImageTk.PhotoImage(Image.open(self.path))

        #The Label widget is a standard Tkinter widget used to display a text or image on the screen.
        self.panel = Label(root, image = self.img)

        #The Pack geometry manager packs widgets in rows or columns.
        self.panel.pack(side = "right", fill = "both", expand = "no")

        Label(self,
              text = "Copy / Paste the Social Media Post here:",bg="#3355CC",
              ).grid(row = 0, column = 0, sticky = W)
         
        self.socialinput = Text(self, width = 100, height = 10, wrap = WORD)
        self.socialinput.grid(row = 5, column = 0, columnspan = 3)
       
                     
        #create the action button
        self.button = Button(self, text = "Analyze for Post Categories, Topics, and Entities",fg="#FFFFFF" , bg="#FF8000")
        self.button["command"] = self.update_text   # don't don't use parens here
        #bind the event handler
        self.button.grid(row = 8, column = 0, columnspan = 3, sticky = W, padx=9, pady=9)

        """ label for the category output area """
        Label(self,
              text = "Categories"
              ).grid(row = 13, column = 0, sticky = W, padx=30, pady=5)
        Label(self,
              text = "Topics"
              ).grid(row = 13, column = 2, sticky = W, padx=30, pady=5)
        Label(self,
              text = "Entities (e.g. names, businesses, orgs)"
              ).grid(row = 13, column = 3, sticky = W, padx=30, pady=5)
        self.categories = Text(self, width = 40, height = 15, wrap = WORD)
        self.categories.grid(row = 14, column = 0, columnspan = 9, sticky = W,  pady=1)

        self.topic = Text(self, width = 40, height = 15, wrap = WORD)
        self.topic.grid(row = 14, column = 2, columnspan = 1, sticky = W, padx=2, pady=2)

        self.entity = Text(self, width = 40, height = 15, wrap = WORD)
        self.entity.grid(row = 14, column = 3, columnspan = 1) 

      
    def update_text(self):

        """ read in the TextRazor API key  """
        with open('E:/CleverMoe/TextRazor_API_key.txt', 'r') as myfile:
            textrazor.api_key=myfile.read().replace('\n', '')
        print "The Textrazor api key as read from file is  " + textrazor.api_key
        """ Display Entity, Topic and Category information in the text area  """
         
        message = self.socialinput.get(1.0, END)
        client = textrazor.TextRazor(extractors=["entities", "topics"])
        client.set_classifiers(["textrazor_iab"])
        response =client.analyze(message)
        #print "Now print the classifer labels.....\n\n\n\n\n\n\n"
        classify_info = ""
        for category in response.categories():
              classify_info += category.label + "\n"
   
              #print "Category Label is:      " + category.label ,  category.score

        self.categories.delete(0.0, END)
        self.categories.insert(0.0, classify_info)

        """  Now pull the topics for the input text  """
        response =client.analyze(message)
        #print "Now print the topic labels .....\n\n\n\n\n\n\n"
        topics_info = ""
        for topic in response.topics():
              if topic.score > 0.3:
            
                  topics_info += topic.label + "\n"
   
              print "Topic Label is:      " + topic.label, topic.score 
        self.topic.delete(0.0, END)
        self.topic.insert(0.0, topics_info)
      
        """   Now pull the entities    """
        print "Now print the entity ids.....\n\n\n\n\n\n\n"

        entities_info = ""
        for entity in response.entities():
                #print entity.id, entity.relevance_score, entity.confidence_score, entity.freebase_types
          if entity.relevance_score > 0.0:
              print entity.id, entity.relevance_score
              entities_info += entity.id + "\n"
        self.entity.delete(0.0, END)
        self.entity.insert(0.0, entities_info)
             
             

         
        #print self.socialinput.get(1.0, END)   #debug
        
root = Tk()

 
root.title("Clever Moe        Social Media Topic Analysis")
root.geometry("1150x510")

app = Application(root)

root.mainloop()

        
