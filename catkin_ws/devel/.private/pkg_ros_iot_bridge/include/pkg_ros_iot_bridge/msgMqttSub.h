// Generated by gencpp from file pkg_ros_iot_bridge/msgMqttSub.msg
// DO NOT EDIT!


#ifndef PKG_ROS_IOT_BRIDGE_MESSAGE_MSGMQTTSUB_H
#define PKG_ROS_IOT_BRIDGE_MESSAGE_MSGMQTTSUB_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>


namespace pkg_ros_iot_bridge
{
template <class ContainerAllocator>
struct msgMqttSub_
{
  typedef msgMqttSub_<ContainerAllocator> Type;

  msgMqttSub_()
    : timestamp()
    , topic()
    , message()  {
    }
  msgMqttSub_(const ContainerAllocator& _alloc)
    : timestamp()
    , topic(_alloc)
    , message(_alloc)  {
  (void)_alloc;
    }



   typedef ros::Time _timestamp_type;
  _timestamp_type timestamp;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _topic_type;
  _topic_type topic;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _message_type;
  _message_type message;





  typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> const> ConstPtr;

}; // struct msgMqttSub_

typedef ::pkg_ros_iot_bridge::msgMqttSub_<std::allocator<void> > msgMqttSub;

typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgMqttSub > msgMqttSubPtr;
typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgMqttSub const> msgMqttSubConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >::stream(s, "", v);
return s;
}

} // namespace pkg_ros_iot_bridge

namespace ros
{
namespace message_traits
{



// BOOLTRAITS {'IsFixedSize': False, 'IsMessage': True, 'HasHeader': False}
// {'pkg_ros_iot_bridge': ['/home/avinash/catkin_ws/src/pkg_ros_iot_bridge/msg', '/home/avinash/catkin_ws/devel/.private/pkg_ros_iot_bridge/share/pkg_ros_iot_bridge/msg'], 'actionlib_msgs': ['/opt/ros/melodic/share/actionlib_msgs/cmake/../msg'], 'std_msgs': ['/opt/ros/melodic/share/std_msgs/cmake/../msg']}

// !!!!!!!!!!! ['__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_parsed_fields', 'constants', 'fields', 'full_name', 'has_header', 'header_present', 'names', 'package', 'parsed_fields', 'short_name', 'text', 'types']




template <class ContainerAllocator>
struct IsFixedSize< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
{
  static const char* value()
  {
    return "76824121accacb087a76246dc01cbb0b";
  }

  static const char* value(const ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x76824121accacb08ULL;
  static const uint64_t static_value2 = 0x7a76246dc01cbb0bULL;
};

template<class ContainerAllocator>
struct DataType< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
{
  static const char* value()
  {
    return "pkg_ros_iot_bridge/msgMqttSub";
  }

  static const char* value(const ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
{
  static const char* value()
  {
    return "time timestamp\n"
"string topic\n"
"string message\n"
;
  }

  static const char* value(const ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.timestamp);
      stream.next(m.topic);
      stream.next(m.message);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct msgMqttSub_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::pkg_ros_iot_bridge::msgMqttSub_<ContainerAllocator>& v)
  {
    s << indent << "timestamp: ";
    Printer<ros::Time>::stream(s, indent + "  ", v.timestamp);
    s << indent << "topic: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.topic);
    s << indent << "message: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.message);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PKG_ROS_IOT_BRIDGE_MESSAGE_MSGMQTTSUB_H
