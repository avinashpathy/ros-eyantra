; Auto-generated. Do not edit!


(cl:in-package pkg_ros_actions-msg)


;//! \htmlinclude msgTurtleGoal.msg.html

(cl:defclass <msgTurtleGoal> (roslisp-msg-protocol:ros-message)
  ((distance
    :reader distance
    :initarg :distance
    :type cl:fixnum
    :initform 0)
   (angle
    :reader angle
    :initarg :angle
    :type cl:fixnum
    :initform 0))
)

(cl:defclass msgTurtleGoal (<msgTurtleGoal>)
  ())

(cl:defmethod cl:initialize-instance :after ((m <msgTurtleGoal>) cl:&rest args)
  (cl:declare (cl:ignorable args))
  (cl:unless (cl:typep m 'msgTurtleGoal)
    (roslisp-msg-protocol:msg-deprecation-warning "using old message class name pkg_ros_actions-msg:<msgTurtleGoal> is deprecated: use pkg_ros_actions-msg:msgTurtleGoal instead.")))

(cl:ensure-generic-function 'distance-val :lambda-list '(m))
(cl:defmethod distance-val ((m <msgTurtleGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pkg_ros_actions-msg:distance-val is deprecated.  Use pkg_ros_actions-msg:distance instead.")
  (distance m))

(cl:ensure-generic-function 'angle-val :lambda-list '(m))
(cl:defmethod angle-val ((m <msgTurtleGoal>))
  (roslisp-msg-protocol:msg-deprecation-warning "Using old-style slot reader pkg_ros_actions-msg:angle-val is deprecated.  Use pkg_ros_actions-msg:angle instead.")
  (angle m))
(cl:defmethod roslisp-msg-protocol:serialize ((msg <msgTurtleGoal>) ostream)
  "Serializes a message object of type '<msgTurtleGoal>"
  (cl:let* ((signed (cl:slot-value msg 'distance)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
  (cl:let* ((signed (cl:slot-value msg 'angle)) (unsigned (cl:if (cl:< signed 0) (cl:+ signed 256) signed)))
    (cl:write-byte (cl:ldb (cl:byte 8 0) unsigned) ostream)
    )
)
(cl:defmethod roslisp-msg-protocol:deserialize ((msg <msgTurtleGoal>) istream)
  "Deserializes a message object of type '<msgTurtleGoal>"
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'distance) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
    (cl:let ((unsigned 0))
      (cl:setf (cl:ldb (cl:byte 8 0) unsigned) (cl:read-byte istream))
      (cl:setf (cl:slot-value msg 'angle) (cl:if (cl:< unsigned 128) unsigned (cl:- unsigned 256))))
  msg
)
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql '<msgTurtleGoal>)))
  "Returns string type for a message object of type '<msgTurtleGoal>"
  "pkg_ros_actions/msgTurtleGoal")
(cl:defmethod roslisp-msg-protocol:ros-datatype ((msg (cl:eql 'msgTurtleGoal)))
  "Returns string type for a message object of type 'msgTurtleGoal"
  "pkg_ros_actions/msgTurtleGoal")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql '<msgTurtleGoal>)))
  "Returns md5sum for a message object of type '<msgTurtleGoal>"
  "9f2f798034d31200675698594323e8ee")
(cl:defmethod roslisp-msg-protocol:md5sum ((type (cl:eql 'msgTurtleGoal)))
  "Returns md5sum for a message object of type 'msgTurtleGoal"
  "9f2f798034d31200675698594323e8ee")
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql '<msgTurtleGoal>)))
  "Returns full string definition for message of type '<msgTurtleGoal>"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# goal~%int8 distance~%int8 angle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:message-definition ((type (cl:eql 'msgTurtleGoal)))
  "Returns full string definition for message of type 'msgTurtleGoal"
  (cl:format cl:nil "# ====== DO NOT MODIFY! AUTOGENERATED FROM AN ACTION DEFINITION ======~%# goal~%int8 distance~%int8 angle~%~%~%"))
(cl:defmethod roslisp-msg-protocol:serialization-length ((msg <msgTurtleGoal>))
  (cl:+ 0
     1
     1
))
(cl:defmethod roslisp-msg-protocol:ros-message-to-list ((msg <msgTurtleGoal>))
  "Converts a ROS message object to a list"
  (cl:list 'msgTurtleGoal
    (cl:cons ':distance (distance msg))
    (cl:cons ':angle (angle msg))
))
