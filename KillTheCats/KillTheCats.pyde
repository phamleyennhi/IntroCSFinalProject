add_library('minim')
import os, random, time
path = os.getcwd() # path to the .pyde file
player = Minim(this)


width = 1280
height = 720
#Create class Creature (class Cat and class Student inherit from this class)
class Creature:
    def __init__(self, x, y, r, vx, hp, w, h, img, F):
        self.x = x
        self.y = y
        self.r = r
        self.vx = vx
        self.hp = hp
        self.w = w
        self.h = h
        self.f = 0
        self.img = loadImage(path+"/images/"+img)
        self.F = F

    def display(self):
        self.update()
        if isinstance(self, Cat):
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,(int(self.f)+1)*self.w,self.h)
        elif isinstance(self, Student):
            image(self.img,self.x-40,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,(int(self.f)+1)*self.w,self.h)
        elif isinstance(self, Plate):
            image(self.img,self.x,self.y-self.h//2-20,self.w,self.h,int(self.f)*self.w,0,(int(self.f)+1)*self.w,self.h)
        elif isinstance(self, Dirham):
            image(self.img,self.x-self.w//2,self.y-self.h//2,self.w,self.h,int(self.f)*self.w,0,(int(self.f)+1)*self.w,self.h)

        stroke(255)
        noFill()
        strokeWeight(1)
        #Draw circle for cats and hp bar (based on type of cat)
        if isinstance(self, Cat):
            #ellipse(self.x, self.y, 2*self.r, 2*self.r)
            rect(self.x - self.l//2, self.y - self.r - 30, self.l, 10, 5)
            #fill color to indicate the hp (hp > 2/3: green, 1/3 < hp < 2/3: yellow, hp <1/3: red)
            if self.hp > self.l*2//3:
                fill(0, 255, 0)
            elif self.hp <= self.l*2//3 and self.hp > self.l//3:
                fill(255, 255, 0)
            elif self.hp <= self.l//3:
                fill(255, 0, 0)
            rect(self.x - self.l//2, self.y - self.r - 30, self.hp, 10, 5)
        #elif isinstance(self, Student):
            #ellipse(self.x + 80, self.y, 2*self.r, 2*self.r)
        #elif isinstance(self, Dirham):
            #ellipse(self.x, self.y, 2*self.r, 2*self.r)
    def update(self):
        self.x += self.vx
        self.f = (self.f+0.2)%self.F
        
    def distance (self, target):
        if self.y == target.y:
            return abs(self.x - target.x)
        else:
            return 10000
        
class Cat (Creature):
    def __init__(self, x, y, r, vx, hp, w, h, img, F):
        Creature.__init__(self, x, y, r, vx, hp, w, h, img, F)
        self.l = hp
        self.v0 = vx
        self.catSound = player.loadFile(path+"/sounds/cat.mp3")
    
    #Update the position of the cat and also detect collision with the plate
    def update (self):
        self.x += self.vx
        self.f = (self.f+0.3)%self.F
        for p in g.plates:
            if self.distance (p) <= self.r + p.r: 
                self.hp -= 5
                if self.hp<=0:
                    self.catSound.play()
                    self.catSound.rewind()
                    g.cats.remove(self)
                    del self
                    return
                g.plates.remove(p)
                del p
     
     #Check lose condition (when a cat manages to pass the left boundary of the screen)
    def checkLose(self):
         if self.x - self.r <0:
             g.state="gameover"
    
class Student(Creature):
    def __init__(self, x, y, r, vx, hp, w, h, img, F):
        Creature.__init__(self, x, y, r, vx, hp, w, h, img, F)
    
    
    def update(self):
        #The student will animate only if there is a cat on the line of the student
        for c in g.cats:
            if c.y == self.y:
                self.f = (self.f+0.2)%self.F
                break
            
        #Detect collision with the cat    
        for c in g.cats:
            if self.distance(c) <= self.r + c.r + c.w//2:
                self.hp -= 1
                c.vx = 0
                
        #Remove student if health<0        
        if self.hp <= 0:
            for c in g.cats:
                if c.y == self.y and c.vx==0:
                    c.vx=c.v0
            g.students.remove(self)
            del self
            return
                    
    
    #Shoot a plate between frame 5 and 5.1 (to sync with the animation)
    #when there is a cat on the line of the student
    def shoot(self):
        for c in g.cats:
            if c.y == self.y and self.f>5 and self.f<5.1:
                g.plates.append(Plate(self.x+120,self.y,25,5,0,50,50,"plate0.png",16))
                break
                
class Dirham(Creature):
    def __init__(self, x, y, r, vx, hp, w, h, img, F):
        Creature.__init__(self, x, y, r, vx, hp, w, h, img, F)
        self.vy=self.vx
        self.rate=self.vx
        self.collected=False
        
    def update(self):
        self.y += self.vy
        #The faster the dirham falls, the faster it animates through the sequence of images
        self.f = (self.f+map(self.rate,0.5,2,0.3,0.4))%self.F 
        #Remove the dirham after falling below the bottom of the screen
        if self.y - self.r >= height:
            g.dirhams.remove(self)
            del self
     
        
class Plate(Creature):
    def __init__(self, x, y, r, vx, hp, w, h, img, F):
        Creature.__init__(self, x, y, r, vx, hp, w, h, img, F)
    
    #Remove the plate after passing through the boundary of the screen    
    def removePlate(self):
        if self.x-self.r > width:
            g.plates.remove(self)
            del self
            return
            
class Game:
    def __init__(self):
        self.music = player.loadFile(path+"/sounds/background.mp3")
        self.music.loop()
        self.gameOver = player.loadFile(path+"/sounds/gameover.mp3")
        self.money= 0
        self.students = []
        self.cats = []
        self.plates = []
        self.dirhams = []
        self.buyNewStudent = False
        self.menu=loadImage(path+ "/images/menu.png")
        self.peekcat=loadImage(path+ "/images/peekcat.png")
        self.peekcat1=loadImage(path+ "/images/peekcat1.png")
        self.ypeekcat=0
        self.bg=loadImage(path+ "/images/bg.png")
        
        
        self.state="menu"
        self.lv="1"
        self.cntCat=0
        
        self.frameForDirham=random.randint(20,40)
        
    def display(self):
        image(self.bg,0,0)
        stroke(255,0,0,150)
        strokeWeight(5)
        for i in range(3):
            line(0,240+i*160,width,240+i*160)
        for i in range(9):
            line(160*i,240,160*i,height)
        for c in self.cats:
            c.display()
            c.checkLose()
        for s in self.students:
            s.display()
            s.shoot()
        for p in self.plates:
            p.display()
            p.removePlate()
            
        #Drop a new dirham randomly
        if frameCount%self.frameForDirham==0:
            self.dirhams.append(Dirham(random.uniform(200,width-25), 0, 25, random.uniform(5,10), 0, 50, 50,"dirham.png" ,15))
            self.frameForDirham=random.randint(20,40)        
        for d in self.dirhams:
            d.display()
        strokeWeight(5)
        
        imgS = loadImage(path + "/images/student0.png")
        imgD = loadImage(path+ "/images/dirham.png")
        
        #Draw the box for additional student
        fill(0,150)
        rect(0, 0, 160, 160)
        if self.money<10*len(self.students):
            tint(255,100)
        image(imgS, 0, 0, 160, 160, 0, 0, 200, 160)
        textSize(25)
        fill(255)
        noTint()
        image(imgD, 130,130,25,25,400,0,450,50)
        text(str(10*len(self.students))+"x",125,150)
        
        #Display money counter
        image(self.bg,width-225,0,225,125,1280-255,0,1280,125)
        fill(0,150)
        rect(width-225,0,225,160)
        image(imgD, width-70,55,50,50,400,0,450,50)
        fill(255)
        textSize(75)
        textAlign(RIGHT)
        text(str(self.money)+"x",width-70,100)
        
    #Randomly add new cats into the game    
    def addCat(self):
        cat = random.randint(0,2)
        if cat == 2:
            f = 13
            w = 250
            h = 250
            hp = 100
            vx = -2
        elif cat == 1:
            f = 7
            w = 200
            h = 153
            hp = 150
            vx = -1
        else:
            f = 7
            w = 200
            h = 153
            hp = 50
            vx = -3
        self.cats.append(Cat(width, 240+80*(2*random.randint(0,2)+1), 40, vx, hp, w, h, "cat" + str(cat) +".png", f))
        self.cntCat+=1
                
    #check if the player has enough dirhams to buy a new student
    def buyStudent(self):
        if mouseX in range (0, 200) and mouseY in range (0,160) and self.money >= 10*len(self.students):
            self.buyNewStudent = True
    
    #Check if there is already a student in a slot and drop it down if the slot is empty        
    def dropStudent(self):
        if mouseX in range (width) and mouseY in range (240, height) and self.buyNewStudent == True: 
            for s in self.students:
                if s.x == (mouseX//160)*160 and s.y == (2*((mouseY-240)//160)+1)*80+240:
                    return
            self.students.append(Student((mouseX//160)*160, 240 + (2*((mouseY-240)//160) + 1)*80, 40, 0, 100, 200, 160, "student0.png", 8))
            self.buyNewStudent = False
            self.money -= 10*(len(self.students)-1)
    
    #Increase money inventory whenever a dirham is collected        
    def collectDirham(self):
        for d in self.dirhams:
            if mouseX >= d.x-1.5*d.r and mouseX <= d.x+1.5*d.r and mouseY >= d.y-1.5*d.r and mouseY <= d.y+1.5*d.r:
                self.money+=1
                d.collected=True
                self.dirhams.remove(d)
                del d
                break

    # def checkWin(self):
    #     g.win = False
        
        
g = Game()
imgS = loadImage(path + "/images/student0.png")
def setup():
    size(width,height)
    global font
    font = createFont(path+"/fonts/scratch.ttf",40)

def draw():
    frameRate(60)
    if g.state == "menu":
        image(g.menu,0,0)
        textFont(font)
        textSize(100)
        textAlign(CENTER)
        fill(150,150)
        image(g.peekcat,width/2-125,height-g.ypeekcat)
        if mouseX >= width/2-100 and mouseX <= width/2+100 and mouseY >= 2*height/3-80 and mouseY <= 2*height/3+50:
            fill(255)
            if g.ypeekcat<250:
                g.ypeekcat+=15
        else:
            if g.ypeekcat>0:
                g.ypeekcat-=20
        text("play",width/2, 2*height/3)
    elif g.state == "play":
        background(0)
        thread("mouseClicked")
        g.display()
        if g.lv=="1":
            if frameCount%300==0:
                if g.cntCat<10:
                    g.addCat()
                else:
                    for i in range(6):
                        g.addCat()
        if g.buyNewStudent == True:
            image(imgS, mouseX - 80, mouseY - 60, 160, 160, 0, 0, 200, 160)
            #Draw the potential student being placed into a slot
            if mouseY>240:
                tint(255,100)
                image(imgS, mouseX//160*160, mouseY//160*160+80,160, 160, 0, 0, 200, 160)
                noTint()
    
    elif g.state == "gameover":
        g.gameOver.play()
        g.music.pause()
        time.sleep(4)
        g.music.rewind()
        g.__init__()
        #pass
        
    
def mouseClicked():
    if g.state=="menu":
        if mouseX >= width/2-100 and mouseX <= width/2+100 and mouseY >= 2*height/3-80 and mouseY <= 2*height/3+50:
            g.state="play"
            g.lv="1"
    if mousePressed==True:
        g.collectDirham()
        g.buyStudent()

def mouseReleased():
    g.dropStudent()
