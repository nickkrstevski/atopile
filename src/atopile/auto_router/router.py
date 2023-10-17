import numpy as np
import pygame

class Node:
    def __init__(self, position, layers=None):
        """
        Initialize a Node with a position and an optional list of layers.

        :param position: Coordinates of the Node.
        :param layers: List of Layer objects associated with the Node.
        """
        self.position = np.array(position, dtype=float)  # Ensure position is a float array
        self.layers = layers if layers else []  # Default to an empty list if no layers are provided
        self.influence_radius

    def add_layer(self, layer):
        """
        Add a Layer to the Node.

        :param layer: Layer object to be added.
        """
        self.layers.append(layer)

    def remove_layer(self, layer):
        """
        Remove a Layer from the Node.

        :param layer: Layer object to be removed.
        """
        self.layers.remove(layer)

    def update_position(self, force):
        # Apply force and constraints, and update position
        # print(f"Updating position of Node at {self.position} with force {force}")
        self.position += force  # or any other logic

    def __str__(self):
        """
        String representation of the Node.
        """
        return f"Node(position={self.position}, layers={', '.join(str(layer) for layer in self.layers)})"

class FixedNode(Node):
    def __init__(self, position, layers=None):
        super().__init__(position, layers)

    def update_position(self, force):
        """
        For FixedNode, this method does nothing because FixedNodes do not move.
        """
        pass

class Line:
    def __init__(self, start_position, end_position, k=100, rest_length=100):
        self.start = FixedNode(np.array(start_position))
        self.end = FixedNode(np.array(end_position))
        self.k = k
        self.rest_length = rest_length
        self.nodes = self._generate_nodes()

    def _generate_nodes(self):
        """
        Generate nodes every 100 units between start and end, including start and end which are FixedNodes.
        """
        nodes = [self.start]
        total_distance = np.linalg.norm(self.end.position - self.start.position)
        num_intervals = int(total_distance / self.rest_length)
        for i in range(1, num_intervals):
            fraction = i / num_intervals
            position = (1 - fraction) * self.start.position + fraction * self.end.position
            nodes.append(Node(position))
        nodes.append(self.end)
        return nodes

    def update_positions(self):
        for node in self.nodes:
            node.update_position()

class Anchor:
    """
    Represents an anchoring point on a component. Lines can be attached to anchors.
    """
    def __init__(self, position):
        self.position = np.array(position, dtype=float)
        self.attached_lines = []  # Lines that are attached to this anchor

    def attach_line(self, line):
        self.attached_lines.append(line)

class Component:
    """
    Represents a physical component with anchor points.
    """
    def __init__(self, initial_position, color):
        self.position = np.array(initial_position, dtype=float)  # Component's position
        self.color = color  # Visual representation color
        self.anchors = []  # List of Anchor objects

    def add_anchor(self, relative_position):
        """
        Adds an anchor to the component at a position relative to the component's position.
        """
        absolute_position = self.position + relative_position
        anchor = Anchor(absolute_position)
        self.anchors.append(anchor)
        return anchor  # Return the anchor so it can be used immediately if needed

    def update(self):
        """
        Update the component's state. This method should be called every frame.
        """
        pass  # Implement movement logic, if any

    def draw(self):
        """
        Render the component. You might want to use some graphics library for this.
        """
        pass  # Implement rendering logic

class Board:
    def __init__(self, lines):
        self.lines = lines  # a list of Line objects

    def update(self):
        PhysicsEngine.update_positions(self.lines)

class Layer:
    def __init__(self, name, properties):
        """
        Initialize a Layer with a name and set of properties.

        :param name: Name of the layer (e.g. 'Top', 'Bottom', 'Inner1', etc.)
        :param properties: Dictionary holding various properties of the layer.
        """
        self.name = name
        self.properties = properties  # Dictionary of properties, can include things like thickness, material, etc.

    def __str__(self):
        """
        String representation of the Layer.
        """
        return f"Layer(name={self.name}, properties={self.properties})"

class PhysicsEngine:
    @staticmethod
    def calculate_repulsion(positions, constant=1.0, epsilon=1e-6):
        """Calculate repulsion forces between all pairs of positions."""
        delta = positions[:, None, :] - positions[None, :, :]
        distances = np.sqrt((delta ** 2).sum(axis=-1)) + epsilon
        forces = constant / (distances ** 2)
        # Make sure nodes don't exert force on themselves
        np.fill_diagonal(forces, 0)
        return forces, delta

    @staticmethod
    def calculate_tension(positions, rest_length, k=1.0):
        """Calculate tension forces between neighboring nodes."""
        delta = positions[1:] - positions[:-1]
        distances = np.linalg.norm(delta, axis=1)
        forces = k * (distances - rest_length)
        return forces, delta

    @classmethod
    def update_positions(cls, positions, repulsion_constant=1, tension_k=1, rest_length=30):
        """Calculate net forces and update node positions."""
        repulsion_forces, repulsion_delta = cls.calculate_repulsion(positions, constant=repulsion_constant)
        tension_forces, tension_delta = cls.calculate_tension(positions, rest_length, k=tension_k)

        # Calculate net forces (you need to expand this based on how you combine tension and repulsion)
        # This is just a starting point, you need to handle the vector nature of forces
        net_forces = repulsion_forces + tension_forces

        # Update positions based on net forces (you may want to use some time step or damping factor here)
        new_positions = positions + net_forces

        return new_positions

#visualizer
from abc import ABC, abstractmethod
class VisualizationEngine(ABC):
    @abstractmethod
    def initialize(self):
        pass

    @abstractmethod
    def draw_node(self, node):
        pass

    @abstractmethod
    def draw_line(self, line):
        pass

    @abstractmethod
    def update_display(self):
        pass

    @abstractmethod
    def handle_events(self):
        pass

class PygameVisualizationEngine(VisualizationEngine):
    def initialize(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.clear_display()

    def draw_node(self, node):
        pygame.draw.circle(self.screen, (0, 0, 255), node.position, 10)
        # Add any other drawing logic for nodes here

    def draw_line(self, line):
        for i in range(len(line.nodes)-1):
            start_pos = line.nodes[i].position.astype(int)
            end_pos = line.nodes[i+1].position.astype(int)
            pygame.draw.line(self.screen, (0, 0, 0), start_pos, end_pos, 1)

    def update_display(self):
        pygame.display.flip()

    def clear_display(self):
        self.screen.fill((255, 255, 255))

    def handle_events(self):
        global running
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()

k = 0.01
c = 30
rest_length = 30
def main(board):
    visualization_engine = PygameVisualizationEngine()
    visualization_engine.initialize()

    simulation_steps_per_frame = 1000  # Number of physics simulation steps per frame of animation

    running = True
    while running:
        for _ in range(simulation_steps_per_frame):
            board.update()  # Update positions based on forces

        visualization_engine.clear_display()
        for line in board.lines:
            visualization_engine.draw_line(line)
            for node in line.nodes:
                visualization_engine.draw_node(node)

        visualization_engine.update_display()
        visualization_engine.handle_events()

lines =  [Line(start_position=[100, 100], end_position=[300, 100], k=k, rest_length=rest_length),
          Line(start_position=[100, 200], end_position=[300, 200], k=k, rest_length=rest_length)]

board = Board(lines)
# main(board)
