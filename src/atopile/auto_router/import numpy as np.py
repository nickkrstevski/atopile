import numpy as np
import pygame
repulsion_factor = 10
attraction_factor = 1

class Node:
    def __init__(self, position, layers=None, attraction_radius=100,replusion_radius=50, fixed=False):
        """
        Initialize a Node with a position and an optional list of layers.

        :param position: Coordinates of the Node.
        :param layers: List of Layer objects associated with the Node.
        """
        self.position = np.array(position, dtype=float)  # Ensure position is a float array
        self.layers = layers if layers else []  # Default to an empty list if no layers are provided
        self.attraction_radius = attraction_radius
        self.repulsion_radius = replusion_radius
        self.fixed = fixed
        self.force = np.zeros(2)

    def distance_to(self, other_node):
        return np.linalg.norm(self.position - other_node.position)

    def apply_force(self, force):
        self.force += force  # accumulate force

    def update_position(self):
        if not self.fixed:
            self.position += self.force  # update next_position based on total force
            self.force = np.zeros(2)  # reset force to zero

class Spring:
    def __init__(self, start_node, end_node, k=0.01, rest_length=10):
        self.start_node = start_node
        self.end_node = end_node
        self.k = k
        self.rest_length = rest_length

    def calculate_force(self):
        # calculate distance between nodes
        distance = np.linalg.norm(self.start_node.position - self.end_node.position)
        # calculate spring force
        spring_force = self.k * (distance - self.rest_length)
        # calculate unit vector
        unit_vector = (self.end_node.position - self.start_node.position) / distance
        # calculate spring force vector
        spring_force_vector = spring_force * unit_vector
        # apply force to nodes
        self.start_node.apply_force(spring_force_vector)
        self.end_node.apply_force(-spring_force_vector)

class Line:
    def __init__(self, start_position, end_position, k=1000000, rest_length=10):
        self.start = Node(np.array(start_position),fixed = True)
        self.end = Node(np.array(end_position),fixed = True)
        self.k = k
        self.rest_length = rest_length
        self.nodes = self._generate_nodes()
        self.springs = self._generate_springs()

    def _generate_nodes(self):
        """
        Generate nodes every 100 units between start and end, including start and end which are FixedNodes.
        """
        nodes = [self.start]
        total_distance = np.linalg.norm(self.end.position - self.start.position)
        num_nodes = int(total_distance / self.rest_length)
        for i in range(1, num_nodes):
            nodes.append(Node(self.start.position + i * (self.end.position - self.start.position) / num_nodes))
        nodes.append(self.end)
        return nodes

    def _generate_springs(self):
        springs = []
        for i in range(len(self.nodes) - 1):
            springs.append(Spring(self.nodes[i], self.nodes[i+1]))
        return springs

class Component:
    def __init__(self, lines):
        self.lines = lines
        self.outline = None



def compute_forces(lines):
    # forced between nodes should only apply if not part of the same line
    for line in lines:
        for line2 in lines:
            if line is not line2:
                for node in line.nodes:
                    for node2 in line2.nodes:
                        distance = node.distance_to(node2)
                        if distance < node.repulsion_radius:
                            repulsion_force = ((node.position - node2.position) / distance **2) * repulsion_factor
                            node.apply_force(repulsion_force)
                        elif distance < node.attraction_radius:
                            attraction_force = ((node2.position - node.position) / distance **2) * attraction_factor
                            node.apply_force(attraction_force)

        # spring forces only apply within lines
        for spring in line.springs:
            spring.calculate_force()

def is_point_in_node(point, node):
    return np.linalg.norm(node.position - point) <= 10  # assuming node is represented by a circle of radius 10

lines = []
lines.append(Line((100, 100), (800, 100)))
lines.append(Line((100, 200), (800, 200)))
lines.append(Line((100, 300), (800, 300)))
lines.append(Line((100, 400), (800, 400)))
lines.append(Line((100, 500), (800, 500)))

#create a canvas
pygame.init()
screen = pygame.display.set_mode((1200, 800))
screen.fill((255, 255, 255))

dragging_node = None  # variable to hold a node reference while dragging

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left mouse button
                mouse_pos = np.array(event.pos, dtype=float)
                for line in lines:
                    for node in line.nodes:
                        if is_point_in_node(mouse_pos, node):
                            dragging_node = node
                            # dragging_node.fixed = True
                            break  # exit the loop once we find the first node under cursor

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Left mouse button
                if dragging_node:
                    # dragging_node.fixed = False
                    dragging_node.position = np.array(dragging_node.position)  # synchronize next_position with position
                    dragging_node = None  # reset the dragging_node variable

        elif event.type == pygame.MOUSEMOTION:
            if dragging_node:
                new_pos = np.array(event.pos, dtype=float)  # update node position to mouse position
                dragging_node.position = new_pos
                dragging_node.position = np.array(new_pos)  # synchronize next_position with position

    for x in range(10):
        compute_forces(lines)

    for line in lines:
        for node in line.nodes:
            if node.force is not np.zeros(2):
                node.update_position()
    # draw the particle
    screen.fill((255, 255, 255))
    for line in lines:
        for node in line.nodes:
            # print(node.position)
            # pygame.draw.circle(screen, (0, 200, 0), (int(node.position[0]), int(node.position[1])), node.attraction_radius, 1)
            # pygame.draw.circle(screen, (200, 0, 0), (int(node.position[0]), int(node.position[1])), node.repulsion_radius, 1)
            pygame.draw.circle(screen, (0, 0, 0), (int(node.position[0]), int(node.position[1])), 3)
        for spring in line.springs:
            pygame.draw.line(screen, (0, 0, 0), start_pos=(int(spring.start_node.position[0]), int(spring.start_node.position[1])), end_pos=(int(spring.end_node.position[0]), int(spring.end_node.position[1])), width=1)


    # for spring in springs:
        # pygame.draw.line(screen, (0, 0, 0), (int(spring.start_node.position), int(spring.end_node.position)))
    pygame.display.flip()
