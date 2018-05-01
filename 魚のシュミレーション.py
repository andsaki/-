from tkinter import * 
import time, random 
FIELD_X,FIELD_Y = 300,300 
tk = Tk()
size = 8
aboid = 20
parallel = 40
centripetal = 60

canvas = Canvas(tk, width=FIELD_X*1, height=FIELD_Y*1)
canvas.pack() 

class World:
    def __init__(self): 
        self.fishes = []
        self.mushroom = set()
        self.Mushrooms = None

    def add_hunter(self,klass,x,y):
        self.fishes.append(klass(x,y,self))
        

    def step(self):

        fish_posi = []
        for fish in self.fishes:
            fish_posi.append((fish.x, fish.y))
        for fish in self.fishes:
            fish_visi = []
            
            for x in range(int(fish.x)-centripetal,int(fish.x)+centripetal):
                for y in range(int(fish.y)-centripetal,int(fish.y)+centripetal):
                    
                    fish_visi.append((x, y))
            for a in fish_posi:
                if a in fish_visi:
                    s = len(a)
                    if s == 0:
                        fish.state = "searching"
                    else:
                        fish.state == "finding"
                    if a != (fish.x,fish.y):
                        
                        fish.action(a)
    
        if fish.state == "searching":
            for fish in self.fishes:
                fish.change_dir()
            
        for fish in self.fishes:
            fish.render()
        tk.update()
        tk.update_idletasks()
        canvas.delete("all")
        

    def start(self,n_steps): 
        self.add_hunter(Fish,0,0)
        self.add_hunter(Fish,45,45)
        self.add_hunter(Fish,45,0)
        #self.add_hunter(Fish,90,90)
        #self.add_hunter(Fish,400,400)
        #self.add_hunter(Fish,500,500)
        for x in range(n_steps):
            self.step()

   

class AbstractFish:
    def __init__(self,x,y,world):
        self.x, self.y = x, y
        self.vx, self.vy = 1, 1
        self.world = world
        self.state = "searching"

    def move(self):
        self.fieldstep()
        self.x = (self.x + self.vx)
        self.y = (self.y + self.vy)
        


    
    def fieldstep(self):
        if self.x < 0:
            
            if self.vx < 0:
                self.vx = -self.vx
        elif self.x + size > FIELD_X:
            
            if self.vx > 0:
                self.vx = -self.vx

        elif self.y < 0:
            
            if self.vy < 0:
                self.vy = -self.vy
        elif self.y + size > FIELD_Y:
            
            if self.vy > 0:
                self.vy = -self.vy
            

        

    def change_dir(self):
        raise NotImplementedError("subclass responsibility")

    def render(self):

        
        
        canvas.create_rectangle(self.x, self.y,
                                self.x+size, self.y+size, fill="black", outline="black")

        

    def __str__(self):
        return "{}:pos =({}, {})".format(self.__class__.__name__,
                                         self.x, self.y) # self.__class__.__name__でクラス名が取得できる。

class Fish(AbstractFish):
    def __init__(self,x,y,world):
        super(Fish,self).__init__(x,y,world)
        


    def action(self,posi):
        if (self.x,self.y) in posi:
            posi.remove((self.x,self.y))
            print("t")
        
        a = posi[0]
        b = posi[1]
        x = self.x
        y = self.y
        l = (x-a)**2+(y-b)**2
        if l <= aboid**2:
            self.aboid(posi)
        elif aboid < l and l <= parallel**2:
            self.parallel(posi)
                
        elif parallel < l and l <= centripetal**2:
            self.centripetal(posi)

    def aboid(self,posi):
        a = posi[0] - self.x
        b = posi[1] - self.y
        r=random.random()
        if r <= 0.1:
            if a != 0 and b == 0:
                ex = -a/abs(a)
                ey = 0
            elif a == 0 and b != 0:
                ex = 0
                ey = -b/abs(b)
            elif a == 0 and b == 0:
                dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
                C = random.choice(dirs)
                
                ex = C[0]
                ey = C[1]
            else:
                
                ex = -a/abs(a)
                ey = b/abs(b)
            self.vx = ex
            self.vy = ey
            self.move()
        elif 0.2 < r and r <= 0.3:
            if a != 0 and b == 0:
                ex = -a/abs(a)
                ey = 0
            elif a == 0 and b != 0:
                ex = 0
                ey = -b/abs(b)
            elif a == 0 and b == 0:
                dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
                C = random.choice(dirs)
                
                ex = C[0]
                ey = C[1]
            else:
            
                ex = a/abs(a)
                ey = -b/abs(b)
            self.vx = ex
            self.vy = ey
            self.move()

        else:
            self.change_dir()

        

    def parallel(self,posi):
        
        r=random.random()
        if r <= 0.5:
            
            self.move()

        else:
            self.change_dir()
        
            
    def centripetal(self,posi):
        a = posi[0] - self.x
        b = posi[1] - self.y
        r=random.random()
        if r <= 0.4:
            if a != 0 and b == 0:
                ex = -a/abs(a)
                ey = 0
            elif a == 0 and b != 0:
                ex = 0
                ey = -b/abs(b)
            else:
                ex = a/abs(a)
                ey = b/abs(b)
            self.vx = ex
            self.vy = ey
            self.move()

        else:
            self.change_dir()
        

        
    def change_dir(self):
        dirs=[(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        ind=dirs.index((self.vx,self.vy))
        r=random.random()
        if r<0.1:
            if r<0.05:
            
                newInd=(ind+1)%8
                
            else:
                newInd=(ind-1)%8
        else:
            newInd=ind
        self.vx,self.vy = dirs[newInd]
        self.move()
            
    


    

    def render(self):

        
        canvas.create_rectangle(self.x, self.y,
                                self.x+size, self.y+size, fill="green", outline="green")

        





        

world = World()
world.start(10000)
