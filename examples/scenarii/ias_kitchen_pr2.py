from morse.builder import *

# Append NavPR2 robot to the scene
james = NavPR2()
james.add_interface('ros')
james.translate(x=0.1, y=2.7)

# Keyboard control
keyboard = Keyboard()
james.append(keyboard)

human = Human()
human.rotate(z=-3.0)

#
# Add passive objects
#

cornflakes = PassiveObject('props/kitchen_objects.blend', 'Cornflakes')
cornflakes.setgraspable()
cornflakes.translate(x=1.37, y=0.5, z=0.9)

fork = PassiveObject('props/kitchen_objects.blend', 'Fork')
fork.setgraspable()
fork.translate(x=1.38, y=0.5, z=0.86)
fork.rotate(z=1.45)

knife = PassiveObject('props/kitchen_objects.blend', 'Knife')
knife.setgraspable()
knife.translate(x=1.39, y=0.5, z=0.86)
knife.rotate(z=1.45)

plate = PassiveObject('props/kitchen_objects.blend', 'Plate')
plate.setgraspable()
plate.translate(x=-1.36, y=2.27, z=0.86)
plate.rotate(z=1.45)

#bread = PassiveObject('props/kitchen_objects.blend', 'Bread')
#bread.setgraspable()
#bread.translate(x=0.5, y=1.97, z=0.86)
#bread.rotate(z=1.45)

bowl = PassiveObject('props/kitchen_objects.blend', 'Bowl')
bowl.setgraspable()
bowl.translate(x=-1.38, y=2.30, z=0.86)
bowl.rotate(z=1.45)

jam = PassiveObject('props/kitchen_objects.blend', 'Jam')
jam.setgraspable()
jam.translate(x=1.33, y=0.45, z=0.86)
jam.rotate(z=1.45)

nutella = PassiveObject('props/kitchen_objects.blend', 'Nutella')
nutella.setgraspable()
nutella.translate(x=1.35, y=0.42, z=0.86)
nutella.rotate(z=1.45)

# Set scenario
env = Environment('tum_kitchen/tum_kitchen')
env.aim_camera([1.0470, 0, 0.7854])



