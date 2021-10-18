// Generated by gencpp from file pkg_ros_iot_bridge/msgRosIotGoal.msg
// DO NOT EDIT!


#ifndef PKG_ROS_IOT_BRIDGE_MESSAGE_MSGROSIOTGOAL_H
#define PKG_ROS_IOT_BRIDGE_MESSAGE_MSGROSIOTGOAL_H


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
struct msgRosIotGoal_
{
  typedef msgRosIotGoal_<ContainerAllocator> Type;

  msgRosIotGoal_()
    : protocol()
    , mode()
    , topic()
    , message()  {
    }
  msgRosIotGoal_(const ContainerAllocator& _alloc)
    : protocol(_alloc)
    , mode(_alloc)
    , topic(_alloc)
    , message(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _protocol_type;
  _protocol_type protocol;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _mode_type;
  _mode_type mode;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _topic_type;
  _topic_type topic;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _message_type;
  _message_type message;





  typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> const> ConstPtr;

}; // struct msgRosIotGoal_

typedef ::pkg_ros_iot_bridge::msgRosIotGoal_<std::allocator<void> > msgRosIotGoal;

typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgRosIotGoal > msgRosIotGoalPtr;
typedef boost::shared_ptr< ::pkg_ros_iot_bridge::msgRosIotGoal const> msgRosIotGoalConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator1> & lhs, const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator2> & rhs)
{
  return lhs.protocol == rhs.protocol &&
    lhs.mode == rhs.mode &&
    lhs.topic == rhs.topic &&
    lhs.message == rhs.message;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator1> & lhs, const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace pkg_ros_iot_bridge

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "e9cbc8cd1a46fb612c6675b9cee83b82";
  }

  static const char* value(const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0xe9cbc8cd1a46fb61ULL;
  static const uint64_t static_value2 = 0x2c6675b9cee83b82ULL;
};

template<class ContainerAllocator>
struct DataType< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "pkg_ros_iot_bridge/msgRosIotGoal";
  }

  static const char* value(const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
{
  static const char* value()
  {
    return "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======\n"
"# goal\n"
"string protocol\n"
"string mode\n"
"string topic\n"
"string message\n"
;
  }

  static const char* value(const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.protocol);
      stream.next(m.mode);
      stream.next(m.topic);
      stream.next(m.message);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct msgRosIotGoal_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::pkg_ros_iot_bridge::msgRosIotGoal_<ContainerAllocator>& v)
  {
    s << indent << "protocol: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.protocol);
    s << indent << "mode: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.mode);
    s << indent << "topic: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.topic);
    s << indent << "message: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.message);
  }
};

} // namespace message_operations
} // namespace ros

#endif // PKG_ROS_IOT_BRIDGE_MESSAGE_MSGROSIOTGOAL_H