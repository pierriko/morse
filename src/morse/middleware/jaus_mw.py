import logging; logger = logging.getLogger("morse." + __name__)
import pymoos.MOOSCommClient
import morse.core.middleware
import GameLogic

class JAUSClass(morse.core.middleware.MorseMiddlewareClass):
    """ Handle communication between Blender and JAUS."""
      
    def __init__(self):
        """ Initialize JAUS middleware"""
        super(self.__class__,self).__init__()
        logger.info("Middleware initialization")
        #self.m = pymoos.MOOSCommClient.MOOSCommClient()
        # intialize MOOS and MORSE times
        #self.current_MOOS_time=pymoos.MOOSCommClient.MOOSTime()
        self.current_sim_time=GameLogic.current_sim_time
        
        #logger.info("%s" % self.m.GetLocalIPAddress())

        #fundamental_frequency = 10 # [Hz]
        #self.m.Run( "127.0.0.1", 9000, "MORSE_SIM", fundamental_frequency) 
        logger.info("JAUS Middleware initialized")
        

    def __del__(self):
        """ Kill the morse JAUS app."""
        #self.m.Close();
        logger.info("Shutting down JAUS middleware...")
   
    def register_component(self, component_name, component_instance, mw_data):
        """ Generate a new topic to publish the data

        The name of the topic is composed of the robot and sensor names.
        Only useful for sensors.
        """
        logger.info("========== Registering component =================")
        parent_name = component_instance.robot_parent.blender_obj.name

        # Extract the information for this middleware
        # This will be tailored for each middleware according to its needs
        # This is specified in the component_config.py in Blender: [mw_data[0], mw_data[1]]
        function_name = mw_data[1]
        logger.info(" ######################## %s"%parent_name)
        logger.info(" ######################## %s"%component_name )
        
        # make sure the handler function exists
        function = self._check_function_exists(function_name)
        
        # The function exists within this class,
        #  so it can be directly assigned to the instance
        if function != None:
            
            # Add data publish functions to output_functions
            if function_name == "post_message":
                component_instance.output_functions.append(function)
                # Generate one publisher and one topic for each component that is a sensor and uses post_message 
                #self._topics.append(rospy.Publisher(parent_name + "/" + component_name, String))
        
            # Read Strings from a JAUS service    
            elif function_name == "read_message":
                component_instance.input_functions.append(function)
                #func = getattr(self, "callback")
                #self._topics.append(rospy.Subscriber(parent_name + "/" + component_name, String, func, component_instance))
       
            else:
                #Add external module 
                #self._add_method(mw_data, component_instance)
                pass
        else:
            # If there is no such function in this module,
            #  try importing from another one
            try:
                # Insert the method in this class
                function = self._add_method(mw_data, component_instance)
            except IndexError as detail:
                logger.error("Method '%s' is not known, and no external module has been specified. Check the 'component_config.py' file for typos" % function_name)
                return
                
        logger.info("Component registered")

    # Post string messages
    def post_message(self, component_instance):
        """ Publish the data to the JAUS middleware
        """
        logger.debug("Posting unkown message to the JAUS middleware.")
        parent_name = component_instance.robot_parent.blender_obj.name

    def read_message(self, component_instance):
        """ read a command message from the database and send to the simulator???"""
        logger.debug("Read message called.")


    def default_action(self):
        pass