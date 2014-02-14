import pygame

import gummworld2
from gummworld2 import data, State, BasicMap, BasicLayer, SpatialHash

import game, terrainnodes, settings
from terrainnodes import issolid


class TerrainLoader(gummworld2.Engine):
    
    def __init__(self, *args, **kwargs):
        self.terrain_args = args
        self.terrain_kwargs = kwargs
        
        window_title = 'Loading...'
        
        super(TerrainLoader, self).__init__(
            caption=window_title,
            resolution=settings.resolution,
            update_speed=60,
            frame_speed=60,
        )
        
        # Fonts and colors
        font_path = data.filepath('font', 'Vera.ttf')
        self.font1 = pygame.font.Font(font_path, 28)
        self.font2 = pygame.font.Font(font_path, 20)
        self.screen.fill_color = settings.bgcolor
        self.fgcolor = settings.fgcolor
        self.frame_color = pygame.Color('grey77')
        self.progress1 = pygame.Color(0, 255, 0)
        self.progress2 = pygame.Color(0, 238, 0)
        self.progress3 = pygame.Color(0, 205, 0)
        self.progress4 = pygame.Color(0, 139, 0)
        
        # Data to manage loading progress display
        self.stage = None
        self.prev_stage = None
        self.max = 1.0
        self.val = 1
        self.w = 0
        self.h = 0
        self.nw = 0
        self.nh = 0
        self.stage_info = []
        self.stage_rect = pygame.Rect(0,0, 1,1)
        self.progress_rect = None
        self.areas = None
        
        State.map = Terrain(*self.terrain_args, **self.terrain_kwargs)
        self.clock.schedule_interval(self.get_node, 0)
    
    def get_node(self, dt):
        stage,value = State.map.make_nodes.next()
        if stage == 'about_terrain_objects':
            self.stage = stage
            n,w,h,nw,nh = value
            self.max = float(n)
            self.val = 1
            self.w = w      # width in blocks
            self.h = h      # height in blocks
            self.nw = nw    # node width in pixels
            self.nh = nh    # node height in pixels
            texts = (
                (self.font1, 'Making Terrain Objects'),
                (self.font2, 'Blocks = {0} x {1}'.format(w,h)),
                (self.font2, '1 Block = {0} x {1} pixels'.format(nw,nh)),
                (self.font2, 'Terrain = {0} x {1} pixels'.format(w*nw,h*nh)),
            )
            for font,text in texts:
                im = font.render(text, 1, self.fgcolor)
                self.stage_info.append(im)
                r = im.get_rect()
                if r.w > self.stage_rect.w:
                    self.stage_rect.w = r.w
                self.stage_rect.h += r.h
            screen_rect = self.screen.rect
            self.stage_rect.centerx = screen_rect.centerx
            self.stage_rect.bottom = screen_rect.centery
            self.progress_rect = pygame.Rect(self.stage_rect)
            self.progress_rect.h = self.font1.get_height() / 2
            self.progress_rect.y = self.stage_rect.bottom + self.progress_rect.h
            self.frame_rect = pygame.Rect(self.progress_rect)
            self.frame_rect.inflate_ip(2,2)
            self.frame_rect.center = self.progress_rect.center
        elif stage == 'make_terrain_objects':
            self.stage = stage
            self.val = value
        
        elif stage == 'finished':
            self.stage = stage
            self.stop()
    
    def stop(self):
        self.pop()
        self.push(game.Game())
    
    def update(self, dt):
        self.update_progress()
    
    def update_progress(self):
        if self.stage == 'make_terrain_objects':
            x,y,w,h = pr = self.progress_rect
            v = w * self.val / self.h
            y1 = h*1/10
            y2 = h*5/10
            y3 = h*9/10
            y4 = h*10/10
            self.areas = (
                (x, y,    v, y1),
                (x, y+y1, v, y2-y1),
                (x, y+y2, v, y3-y2),
                (x, y+y3, v, y4-y3),
            )
    
    def draw(self, interp):
        screen = self.screen
        screen.clear()
        self.draw_info(screen)
        screen.flip()
    
    def draw_info(self, screen):
        if self.stage == 'make_terrain_objects':
            x,y = self.stage_rect.topleft
            for im in self.stage_info:
                r = im.get_rect()
                screen.blit(im, (x,y))
                y += im.get_height()
            self.draw_progress(screen)
    
    def draw_progress(self, screen):
        pygame.draw.rect(
            screen.surface, self.frame_color, self.frame_rect, 1)
        screen.surface.fill(self.progress4, self.areas[0])
        screen.surface.fill(self.progress1, self.areas[1])
        screen.surface.fill(self.progress2, self.areas[2])
        screen.surface.fill(self.progress4, self.areas[3])


class Terrain(BasicMap):
    """Create a BasicMap to manage the terrain; the finished object is placed in State.map
    """
    
    NODE_WIDTH,NODE_HEIGHT = terrainnodes.NODE_SIZE()
    
    ## pygame space, top=0 bottom=N based on:
    ## nodes_y = 312
    ## NODE_SIZE = 16,16
    ## Should be an even multiple of NODE_HEIGHT
    SEA_LEVEL = 93 * terrainnodes.NODE_SIZE()[1]
    
    def __init__(self, nodes_x, nodes_y=312, cell_size=64):
        super(Terrain, self).__init__(
            nodes_x, nodes_y, self.NODE_WIDTH, self.NODE_HEIGHT)
        
        if __debug__: print '{0}: creating space'.format(
            self.__class__.__name__)
        space = BasicLayer(self, 0, cell_size)
        self.layers.append(space)
        self.make_nodes = make_terrain_nodes(self.width, self.height, space.add)
        if __debug__: print '{0}: loading map'.format(
            self.__class__.__name__)
    
    def intersect_objects(self, rect, layer=0):
        space = self.layers[layer].objects
        return space.intersect_objects(rect)
    
    def collidesolids(self, rect, layer=0):
        return [o for o in self.intersect_objects(rect, layer) if issolid(o)]
    
    def load(self, filename):
        pass
    
    def save(self, filename):
        pass


def make_terrain_nodes(width, height, addfunc):
    """Make 2D list of nodes
    
    size is in pixels.
    """
    
    myname = make_terrain_nodes.__name__
    
    NODE_WIDTH = Terrain.NODE_WIDTH
    NODE_HEIGHT = Terrain.NODE_HEIGHT
    DIRT = terrainnodes.DIRT
    WATER = terrainnodes.WATER
    AIR = terrainnodes.AIR
    sea_level = Terrain.SEA_LEVEL / NODE_HEIGHT
    
    # Create interactive objects.
    
    if __debug__: print '{0}: creating terrain objects'.format(myname)
    
    # The four blocks of dirt at the edge of the world.
    world_edges = []
    x1 = NODE_WIDTH / 2
    x2 = (width-1) * NODE_WIDTH + NODE_WIDTH / 2
    for i in xrange(5):
        y = (sea_level - i) * NODE_HEIGHT + NODE_HEIGHT / 2
        world_edges.append((x1,y))
        world_edges.append((x2,y))
#    print Terrain.SEA_LEVEL,world_edges; quit()
    
    TYPES = terrainnodes.TYPES
    i = n = height
    yield ('about_terrain_objects', (n,width,height,NODE_WIDTH,NODE_HEIGHT))
    while i > 0:
        i -= 1
        if i >= sea_level:
            typ = DIRT
        else:
            typ = AIR
        j = width
        while j > 0:
            j -= 1
            x = j * NODE_WIDTH + NODE_WIDTH / 2
            y = i * NODE_HEIGHT + NODE_HEIGHT / 2
            if (x,y) in world_edges or typ == DIRT:
                node = TYPES[DIRT]((x,y), True)
            else:
                node = TYPES[typ]((x,y))
            addfunc(node)
        yield ('make_terrain_objects', n-i)
    
    if __debug__: print '{0}: done making terrain'.format(myname)
    
    yield ('finished', None)


if __name__ == '__main__':
    # In an 800x600 window:
    #   25000 / 800 = 62.5 screens x-axis
    #   5000 / 600 = 16.7 screens y-axis
    terrain = Terrain(25000, 5000)
