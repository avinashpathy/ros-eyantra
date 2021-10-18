// Generated by gencpp from file gazebo_msgs/SpawnModelRequest.msg
// DO NOT EDIT!


#ifndef GAZEBO_MSGS_MESSAGE_SPAWNMODELREQUEST_H
#define GAZEBO_MSGS_MESSAGE_SPAWNMODELREQUEST_H


#include <string>
#include <vector>
#include <map>

#include <ros/types.h>
#include <ros/serialization.h>
#include <ros/builtin_message_traits.h>
#include <ros/message_operations.h>

#include <geometry_msgs/Pose.h>

namespace gazebo_msgs
{
template <class ContainerAllocator>
struct SpawnModelRequest_
{
  typedef SpawnModelRequest_<ContainerAllocator> Type;

  SpawnModelRequest_()
    : model_name()
    , model_xml()
    , robot_namespace()
    , initial_pose()
    , reference_frame()  {
    }
  SpawnModelRequest_(const ContainerAllocator& _alloc)
    : model_name(_alloc)
    , model_xml(_alloc)
    , robot_namespace(_alloc)
    , initial_pose(_alloc)
    , reference_frame(_alloc)  {
  (void)_alloc;
    }



   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _model_name_type;
  _model_name_type model_name;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _model_xml_type;
  _model_xml_type model_xml;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _robot_namespace_type;
  _robot_namespace_type robot_namespace;

   typedef  ::geometry_msgs::Pose_<ContainerAllocator>  _initial_pose_type;
  _initial_pose_type initial_pose;

   typedef std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other >  _reference_frame_type;
  _reference_frame_type reference_frame;





  typedef boost::shared_ptr< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> > Ptr;
  typedef boost::shared_ptr< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> const> ConstPtr;

}; // struct SpawnModelRequest_

typedef ::gazebo_msgs::SpawnModelRequest_<std::allocator<void> > SpawnModelRequest;

typedef boost::shared_ptr< ::gazebo_msgs::SpawnModelRequest > SpawnModelRequestPtr;
typedef boost::shared_ptr< ::gazebo_msgs::SpawnModelRequest const> SpawnModelRequestConstPtr;

// constants requiring out of line definition



template<typename ContainerAllocator>
std::ostream& operator<<(std::ostream& s, const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> & v)
{
ros::message_operations::Printer< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >::stream(s, "", v);
return s;
}


template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator==(const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator1> & lhs, const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator2> & rhs)
{
  return lhs.model_name == rhs.model_name &&
    lhs.model_xml == rhs.model_xml &&
    lhs.robot_namespace == rhs.robot_namespace &&
    lhs.initial_pose == rhs.initial_pose &&
    lhs.reference_frame == rhs.reference_frame;
}

template<typename ContainerAllocator1, typename ContainerAllocator2>
bool operator!=(const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator1> & lhs, const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator2> & rhs)
{
  return !(lhs == rhs);
}


} // namespace gazebo_msgs

namespace ros
{
namespace message_traits
{





template <class ContainerAllocator>
struct IsFixedSize< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct IsFixedSize< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> const>
  : FalseType
  { };

template <class ContainerAllocator>
struct IsMessage< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
  : TrueType
  { };

template <class ContainerAllocator>
struct IsMessage< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> const>
  : TrueType
  { };

template <class ContainerAllocator>
struct HasHeader< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
  : FalseType
  { };

template <class ContainerAllocator>
struct HasHeader< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> const>
  : FalseType
  { };


template<class ContainerAllocator>
struct MD5Sum< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "6d0eba5753761cd57e6263a056b79930";
  }

  static const char* value(const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator>&) { return value(); }
  static const uint64_t static_value1 = 0x6d0eba5753761cd5ULL;
  static const uint64_t static_value2 = 0x7e6263a056b79930ULL;
};

template<class ContainerAllocator>
struct DataType< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "gazebo_msgs/SpawnModelRequest";
  }

  static const char* value(const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator>&) { return value(); }
};

template<class ContainerAllocator>
struct Definition< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
{
  static const char* value()
  {
    return "string model_name                 # name of the model to be spawn\n"
"string model_xml                  # this should be an urdf or gazebo xml\n"
"string robot_namespace            # spawn robot and all ROS interfaces under this namespace\n"
"geometry_msgs/Pose initial_pose   # only applied to canonical body\n"
"string reference_frame            # initial_pose is defined relative to the frame of this model/body\n"
"                                  # if left empty or \"world\", then gazebo world frame is used\n"
"                                  # if non-existent model/body is specified, an error is returned\n"
"                                  #   and the model is not spawned\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Pose\n"
"# A representation of pose in free space, composed of position and orientation. \n"
"Point position\n"
"Quaternion orientation\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Point\n"
"# This contains the position of a point in free space\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"\n"
"================================================================================\n"
"MSG: geometry_msgs/Quaternion\n"
"# This represents an orientation in free space in quaternion form.\n"
"\n"
"float64 x\n"
"float64 y\n"
"float64 z\n"
"float64 w\n"
;
  }

  static const char* value(const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator>&) { return value(); }
};

} // namespace message_traits
} // namespace ros

namespace ros
{
namespace serialization
{

  template<class ContainerAllocator> struct Serializer< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
  {
    template<typename Stream, typename T> inline static void allInOne(Stream& stream, T m)
    {
      stream.next(m.model_name);
      stream.next(m.model_xml);
      stream.next(m.robot_namespace);
      stream.next(m.initial_pose);
      stream.next(m.reference_frame);
    }

    ROS_DECLARE_ALLINONE_SERIALIZER
  }; // struct SpawnModelRequest_

} // namespace serialization
} // namespace ros

namespace ros
{
namespace message_operations
{

template<class ContainerAllocator>
struct Printer< ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator> >
{
  template<typename Stream> static void stream(Stream& s, const std::string& indent, const ::gazebo_msgs::SpawnModelRequest_<ContainerAllocator>& v)
  {
    s << indent << "model_name: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.model_name);
    s << indent << "model_xml: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.model_xml);
    s << indent << "robot_namespace: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.robot_namespace);
    s << indent << "initial_pose: ";
    s << std::endl;
    Printer< ::geometry_msgs::Pose_<ContainerAllocator> >::stream(s, indent + "  ", v.initial_pose);
    s << indent << "reference_frame: ";
    Printer<std::basic_string<char, std::char_traits<char>, typename ContainerAllocator::template rebind<char>::other > >::stream(s, indent + "  ", v.reference_frame);
  }
};

} // namespace message_operations
} // namespace ros

#endif // GAZEBO_MSGS_MESSAGE_SPAWNMODELREQUEST_H
