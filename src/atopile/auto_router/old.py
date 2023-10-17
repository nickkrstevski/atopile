import pygame
import sys
import numpy as np

# Initialize Pygame
pygame.init()

# Set up display parameters
width, height = 1000, 700
background_color = (255, 255, 255)  # White background

# Circle parameters
node_circle_radius = 3  # Radius of the nodes on the lines
repulsive_circle_radius = 20  # Radius of the red circle
blue_color = (0, 0, 255)  # Blue circles
red_color = (255, 0, 0)  # Red circle

# Set up the drawing window
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Multiple Spring-Damper with Repulsive Circle')

# Spring, damper, and repulsion parameters
stiffness = 0.053  # Spring constant
damping = .94  # Damping factor
repulsion_constant = 5  # Repulsion force constant
inter_repulsion_constant = 10  # Repulsion force constant between nodes of different lines, set to a desired value

class Component:
    def __init__(self, initial_anchor_positions):
        self.anchor_positions = np.array(initial_anchor_positions)
        self.dragging = False
        self.color = (0, 255, 0)  # Green color for visual representation
        self.angle = 0  # New attribute to store rotation angle

    def rotate(self, angle_degrees):
        """Rotate the component by a specified angle in degrees."""
        center = np.mean(self.anchor_positions, axis=0)
        angle_radians = np.deg2rad(angle_degrees)
        rotation_matrix = np.array([
            [np.cos(angle_radians), -np.sin(angle_radians)],
            [np.sin(angle_radians), np.cos(angle_radians)]
        ])
        # Translate anchors to origin, rotate, then translate back
        self.anchor_positions = np.dot(self.anchor_positions - center, rotation_matrix.T) + center


components = [
    Component(initial_anchor_positions=[[50, 250], [50, 350], [10, 250], [10, 350]]),  # Component 0 with 4 anchors
    Component(initial_anchor_positions=[[450, 250], [450, 350]]),  # Component 1 with 2 anchors
    Component(initial_anchor_positions=[[250, 450], [350, 450]])  # Component 2 with 2 anchors
]

class Line:
    def __init__(self, start_component, start_anchor_idx, end_component, end_anchor_idx, distance_per_node=50):
        self.start_component = start_component
        self.start_anchor_idx = start_anchor_idx
        self.end_component = end_component
        self.end_anchor_idx = end_anchor_idx
        self.distance_per_node = distance_per_node
        self.update_nodes()

    def update_nodes(self):
        # Compute the distance between start and end
        distance = np.linalg.norm(self.end - self.start)
        # Calculate the number of nodes based on distance
        self.num_nodes = max(1, int(distance / self.distance_per_node))  # At least one node
        # Initialize or update node_positions and node_velocities
        self.node_positions = np.linspace(self.start, self.end, self.num_nodes + 2)[1:-1]  # excluding start and end points
        # self.node_velocities = [np.array([0.0, 0.0]) for _ in range(self.num_nodes)]
        self.dragging_nodes = [False for _ in range(self.num_nodes)]

    @property
    def start(self):
        return self.start_component.anchor_positions[self.start_anchor_idx]

    @property
    def end(self):
        return self.end_component.anchor_positions[self.end_anchor_idx]


line1 = Line(start_component=components[0], start_anchor_idx=0, end_component=components[1], end_anchor_idx=0)
line2 = Line(start_component=components[0], start_anchor_idx=1, end_component=components[1], end_anchor_idx=1)
line3_1 = Line(start_component=components[0], start_anchor_idx=2, end_component=components[2], end_anchor_idx=0)
line3_2 = Line(start_component=components[0], start_anchor_idx=3, end_component=components[2], end_anchor_idx=1)
line3_3 = Line(start_component=components[2], start_anchor_idx=0, end_component=components[1], end_anchor_idx=0)

lines = [line1, line2, line3_1, line3_2, line3_3]

# Initial position of the repulsive circle
repulsive_circle_position = np.array([250.0, 300.0])

# Indicator of whether the repulsive circle is being dragged
dragging_repulsive_circle = False

def quadratic_bezier_curve(P0, P1, P2, num_points):
    """Compute Quadratic Bézier Curve for given three points and return interpolated points."""
    points = []
    for t in np.linspace(0, 1, num_points):
        point = (1 - t)**2 * P0 + 2 * (1 - t) * t * P1 + t**2 * P2
        points.append(point)
    return np.array(points)

def cubic_bezier_curve(P0, P1, P2, P3, num_points):
    """Compute Cubic Bézier Curve for given four points and return interpolated points."""
    points = []
    for t in np.linspace(0, 1, num_points):
        point = (1 - t)**3 * P0 + 3 * (1 - t)**2 * t * P1 + 3 * (1 - t) * t**2 * P2 + t**3 * P3
        points.append(point)
    return np.array(points)

def catmull_rom_spline(P0, P1, P2, P3, num_points):
    """Compute Catmull-Rom spline for given four points and return interpolated points."""
    points = []
    alpha = 0.5

    for t in np.linspace(0, 1, num_points):
        a1 = (1-t)*P0 + t*P1
        a2 = (1-t)*P1 + t*P2
        a3 = (1-t)*P2 + t*P3

        b1 = (1-t)*a1 + t*a2
        b2 = (1-t)*a2 + t*a3

        c = (1-t)*b1 + t*b2

        points.append(c)

    return np.array(points)




# Game loop
# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for component in components:
                for idx, anchor in enumerate(component.anchor_positions):
                    if np.linalg.norm(anchor - np.array(event.pos)) <= node_circle_radius:
                        component.dragging = True
                        component.dragging_anchor_idx = idx  # store index of anchor being dragged
        elif event.type == pygame.MOUSEBUTTONUP:
            for component in components:
                component.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            for component in components:
                if component.dragging:
                    displacement = np.array(event.pos) - component.anchor_positions[component.dragging_anchor_idx]
                    component.anchor_positions += displacement

        for component in components:
            if component.dragging:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_r]:
                    component.rotate(45)  # Rotate by 45 degrees


    # for line in lines:
    #     line.update_nodes()

    # Force calculation and position update loop
    for line in lines:
        for i in range(line.num_nodes):
            if not line.dragging_nodes[i]:
                # Find target position based on neighbors
                if i > 0 and i < line.num_nodes - 1:  # Nodes that are not on the ends
                    target_position = (line.node_positions[i - 1] + line.node_positions[i + 1]) / 2
                elif i == 0:  # First node
                    target_position = (line.start + line.node_positions[i + 1]) / 2
                else:  # Last node
                    target_position = (line.node_positions[i - 1] + line.end) / 2

                # Calculate repulsion effects from other nodes and adjust target_position
                for other_line in lines:
                    if other_line != line:
                        for other_node_position in other_line.node_positions:
                            distance_to_other_node = np.linalg.norm(target_position - other_node_position) + 1e-6
                            repulsion_direction = (target_position - other_node_position) / distance_to_other_node
                            repulsion_force = inter_repulsion_constant / distance_to_other_node**2
                            target_position += repulsion_force * repulsion_direction * 100  # adjust scaling as needed

                # Calculate repulsion effect from repulsive circle and adjust target_position
                distance_to_repulsive_circle = np.linalg.norm(target_position - repulsive_circle_position) + 1e-6
                repulsion_direction = (target_position - repulsive_circle_position) / distance_to_repulsive_circle
                repulsion_force = repulsion_constant / distance_to_repulsive_circle**2
                target_position += repulsion_force * repulsion_direction * 1000  # adjust scaling as needed

                # Set the node position
                line.node_positions[i] = target_position


    # Drawing loop for each line and node
    screen.fill(background_color)
    # Drawing loop
    for component in components:
        for anchor in component.anchor_positions:
            pygame.draw.circle(screen, component.color, anchor.astype(int), node_circle_radius)

    # Drawing loop for each line and node

    for line in lines:
        # Concatenate all nodes for the line
        all_nodes = np.vstack((line.start[np.newaxis, :], line.node_positions, line.end[np.newaxis, :]))

        # Generate the full list of spline points
        spline_points = []
        for i in range(len(all_nodes) - 3):
            P0, P1, P2, P3 = all_nodes[i], all_nodes[i + 1], all_nodes[i + 2], all_nodes[i + 3]
            points = catmull_rom_spline(P0, P1, P2, P3, 20)
            spline_points.extend(points)

        # Draw lines between adjacent spline points
        for p in range(len(spline_points) - 1):
            pygame.draw.line(screen, (0, 0, 0), spline_points[p], spline_points[p + 1], 1)


    pygame.draw.circle(screen, red_color, repulsive_circle_position.astype(int), repulsive_circle_radius)
        # Drawing loop for each line and node
    for component in components:
        min_x = min(component.anchor_positions[:, 0])
        max_x = max(component.anchor_positions[:, 0])
        min_y = min(component.anchor_positions[:, 1])
        max_y = max(component.anchor_positions[:, 1])

        width = max(10, max_x - min_x)
        height = max(10, max_y - min_y)

        # Adjust min_x and min_y if width or height adjustments were made
        if width == 10:
            min_x = (min_x + max_x) / 2 - 5
        if height == 10:
            min_y = (min_y + max_y) / 2 - 5

        pygame.draw.rect(screen, component.color, (min_x, min_y, width, height), 2)  # The '2' here is the width of the rectangle's border

        for anchor in component.anchor_positions:
            pygame.draw.circle(screen, component.color, anchor.astype(int), node_circle_radius)

    pygame.display.flip()

