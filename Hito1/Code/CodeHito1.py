import csv

class Videogame:
  def __init__(self, id, name, platform, year, genre, publisher):
    self.id = id
    self.name = name
    self.platform = platform
    self.genre = genre
    self.year = year
    self.publisher = publisher
  
  def getId(self):      
    return self.id  

  def getName(self):      
     return self.name   


  def getPlatform(self):
    return self.platform


  def getGenre(self):
    return self.genre

  def getYear(self):
    return self.year

  def getPublisher(self):
    return self.publisher


videogames = []

with open("vgsales.csv") as f:
  reader = csv.reader(f)
  for row in reader:
    videogames.append(Videogame(row[0],row[1],row[2],row[3],row[4],row[5]))

videogames.pop(0)

def createNodesCSV():
    
    vgnodes=[]
    rowtop=["ID","Label"]
    vgnodes.append(rowtop)

    for i in range(len(videogames)):
       if(i==1500):break
       row=[]
       row.append(videogames[i].getId())
       row.append(videogames[i].getName())
       vgnodes.append(row)


    with open("vgnodes.csv","w",newline="")as file:
        writer = csv.writer(file,delimiter=",")
        writer.writerows(vgnodes)

def compare_videogames(videogame1, videogame2):
  points = 0
  if videogame1.platform == videogame2.platform:
    points+=5
  if videogame1.genre == videogame2.genre:
    points+=5
  if abs(int(videogame1.year) - int(videogame2.year)) <= 5:
    points+=5
  elif abs(int(videogame1.year) - int(videogame2.year)) <= 15:
    points+=2
  if videogame1.publisher == videogame2.publisher:
    points+=3
  return 19 - points

def generateLinksCSV():
  vglinks=[]
  rowtop=["Source","Target","Weight","Label","Type"]
  vglinks.append(rowtop)

  for i in range(len(videogames)):
    vg1=videogames[i]
    if(i==1500):break
    for j in range(len(videogames)):
      if(i!=j):
        if(j==1500):break
        vg2=videogames[j]
        row=[]
        row.append(vg1.getId())
        row.append(vg2.getId())
        row.append(compare_videogames(vg1,vg2))
        row.append("-")
        row.append("Directed")
        print(row)
        vglinks.append(row)
   
  
    
      
  with open("vglinks.csv","w",newline="")as file:
    writer = csv.writer(file,delimiter=",")
    writer.writerows(vglinks)

createNodesCSV()
