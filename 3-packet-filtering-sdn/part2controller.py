from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

class Firewall (object):
  """
  A Firewall object is created for each switch that connects.
  A Connection object for that switch is passed to the __init__ function.
  """
  def __init__ (self, connection):
    # Keep track of the connection to the switch so that we can
    # send it messages!
    self.connection = connection

    # This binds our PacketIn event listener
    connection.addListeners(self)

    # Action that will accept any packet with ipv4 src and dest @, and icmp protocol
    first_rule = of.ofp_flow_mod() # Saying that we are giving a flow table entry
    # Starting message composition
    first_rule.priority = 3000 # Top priority
    first_rule.match.dl_type = 0x0800 # Specifying for ipv4
    first_rule.match.nw_proto = 1 # Specifying for IMPC
    first_rule.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD)) # Return to physical protocol
    self.connection.send(first_rule) # Send message

    # Action that will accept any packet from any src and dest @, and arp protocol
    second_rule = of.ofp_flow_mod()
    # Starting message composition
    second_rule.priority = 2000 # Middle priority
    second_rule.match.dl_type = 0x0806 # No need to specify nw_proto, just by the dl_type
    second_rule.actions.append(of.ofp_action_output(port = of.OFPP_FLOOD)) 
    self.connection.send(second_rule) # Send message
    
    # Action that will drop any packet that has ipv4 src and dest @, but uses other protocol that icmp or arp
    third_rule = of.ofp_flow_mod()
    # Starting message composition
    third_rule.priority = 1000 # Some priority
    third_rule.match.dl_type = 0x0800 # Specifying ipv4
    third_rule.buffer_id = None
    self.connection.send(third_rule) # Send message

  def _handle_PacketIn (self, event):
    """
    Packets not handled by the router rules will be
    forwarded to this method to be handled by the controller
    """

    packet = event.parsed # This is the parsed packet data.
    if not packet.parsed:
      log.warning("Ignoring incomplete packet")
      return

    packet_in = event.ofp # The actual ofp_packet_in message.
    print ("Unhandled packet :" + str(packet.dump()))

def launch ():
  """
  Starts the component
  """
  def start_switch (event):
    log.debug("Controlling %s" % (event.connection,))
    Firewall(event.connection)
  core.openflow.addListenerByName("ConnectionUp", start_switch)
