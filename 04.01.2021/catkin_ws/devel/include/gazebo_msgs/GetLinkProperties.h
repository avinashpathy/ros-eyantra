// Generated by gencpp from file gazebo_msgs/GetLinkProperties.msg
// DO NOT EDIT!


#ifndef GAZEBO_MSGS_MESSAGE_GETLINKPROPERTIES_H
#define GAZEBO_MSGS_MESSAGE_GETLINKPROPERTIES_H

#include <ros/service_traits.h>


#include <gazebo_msgs/GetLinkPropertiesRequest.h>
#include <gazebo_msgs/GetLinkPropertiesResponse.h>


namespace gazebo_msgs
{

struct GetLinkProperties
{

typedef GetLinkPropertiesRequest Request;
typedef GetLinkPropertiesResponse Response;
Request request;
Response response;

typedef Request RequestType;
typedef Response ResponseType;

}; // struct GetLinkProperties
} // namespace gazebo_msgs


namespace ros
{
namespace service_traits
{


template<>
struct MD5Sum< ::gazebo_msgs::GetLinkProperties > {
  static const char* value()
  {
    return "0e06a70386d0ee3fb880c02f23fcd821";
  }

  static const char* value(const ::gazebo_msgs::GetLinkProperties&) { return value(); }
};

template<>
struct DataType< ::gazebo_msgs::GetLinkProperties > {
  static const char* value()
  {
    return "gazebo_msgs/GetLinkProperties";
  }

  static const char* value(const ::gazebo_msgs::GetLinkProperties&) { return value(); }
};


// service_traits::MD5Sum< ::gazebo_msgs::GetLinkPropertiesRequest> should match
// service_traits::MD5Sum< ::gazebo_msgs::GetLinkProperties >
template<>
struct MD5Sum< ::gazebo_msgs::GetLinkPropertiesRequest>
{
  static const char* value()
  {
    return MD5Sum< ::gazebo_msgs::GetLinkProperties >::value();
  }
  static const char* value(const ::gazebo_msgs::GetLinkPropertiesRequest&)
  {
    return value();
  }
};

// service_traits::DataType< ::gazebo_msgs::GetLinkPropertiesRequest> should match
// service_traits::DataType< ::gazebo_msgs::GetLinkProperties >
template<>
struct DataType< ::gazebo_msgs::GetLinkPropertiesRequest>
{
  static const char* value()
  {
    return DataType< ::gazebo_msgs::GetLinkProperties >::value();
  }
  static const char* value(const ::gazebo_msgs::GetLinkPropertiesRequest&)
  {
    return value();
  }
};

// service_traits::MD5Sum< ::gazebo_msgs::GetLinkPropertiesResponse> should match
// service_traits::MD5Sum< ::gazebo_msgs::GetLinkProperties >
template<>
struct MD5Sum< ::gazebo_msgs::GetLinkPropertiesResponse>
{
  static const char* value()
  {
    return MD5Sum< ::gazebo_msgs::GetLinkProperties >::value();
  }
  static const char* value(const ::gazebo_msgs::GetLinkPropertiesResponse&)
  {
    return value();
  }
};

// service_traits::DataType< ::gazebo_msgs::GetLinkPropertiesResponse> should match
// service_traits::DataType< ::gazebo_msgs::GetLinkProperties >
template<>
struct DataType< ::gazebo_msgs::GetLinkPropertiesResponse>
{
  static const char* value()
  {
    return DataType< ::gazebo_msgs::GetLinkProperties >::value();
  }
  static const char* value(const ::gazebo_msgs::GetLinkPropertiesResponse&)
  {
    return value();
  }
};

} // namespace service_traits
} // namespace ros

#endif // GAZEBO_MSGS_MESSAGE_GETLINKPROPERTIES_H