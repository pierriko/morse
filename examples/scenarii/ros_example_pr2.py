from morse.builder import *

# Append NavPR2 robot to the scene
james = NavPR2()
james.add_interface('ros')
james.translate(x=2.5, y=3.2)

# Keyboard control
keyboard = Keyboard()
james.append(keyboard)

human = Human()
human.translate(x=2.5)

#
# Add passive objects
#

cornflakes = PassiveObject('props/kitchen_objects', 'Cornflakes')
cornflakes.setgraspable()
cornflakes.translate(x=0.5, y=1.67, z=0.9)

fork = PassiveObject('props/kitchen_objects', 'Fork')
fork.setgraspable()
fork.translate(x=0.5, y=1.87, z=0.86)
fork.rotate(z=1.45)

knife = PassiveObject('props/kitchen_objects', 'Knife')
knife.setgraspable()
knife.translate(x=0.5, y=1.97, z=0.86)
knife.rotate(z=1.45)

plate = PassiveObject('props/kitchen_objects', 'Plate')
plate.setgraspable()
plate.translate(x=0.5, y=1.97, z=0.86)
plate.rotate(z=1.45)

#bread = PassiveObject('props/kitchen_objects', 'Bread')
#bread.setgraspable()
#bread.translate(x=0.5, y=1.97, z=0.86)
#bread.rotate(z=1.45)

bowl = PassiveObject('props/kitchen_objects', 'Bowl')
bowl.setgraspable()
bowl.translate(x=0.5, y=1.97, z=0.86)
bowl.rotate(z=1.45)

jam = PassiveObject('props/kitchen_objects', 'Jam')
jam.setgraspable()
jam.translate(x=0.5, y=1.97, z=0.86)
jam.rotate(z=1.45)

nutella = PassiveObject('props/kitchen_objects', 'Nutella')
nutella.setgraspable()
nutella.translate(x=0.5, y=1.97, z=0.86)
nutella.rotate(z=1.45)

# Set scenario
env = Environment('tum_kitchen/tum_kitchen')
env.aim_camera([1.0470, 0, 0.7854])
