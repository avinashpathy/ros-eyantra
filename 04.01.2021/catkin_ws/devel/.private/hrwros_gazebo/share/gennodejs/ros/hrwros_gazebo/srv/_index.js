
"use strict";

let VacuumGripperControl = require('./VacuumGripperControl.js')
let ConveyorBeltControl = require('./ConveyorBeltControl.js')
let AGVControl = require('./AGVControl.js')
let SubmitTray = require('./SubmitTray.js')
let PopulationControl = require('./PopulationControl.js')
let GetMaterialLocations = require('./GetMaterialLocations.js')

module.exports = {
  VacuumGripperControl: VacuumGripperControl,
  ConveyorBeltControl: ConveyorBeltControl,
  AGVControl: AGVControl,
  SubmitTray: SubmitTray,
  PopulationControl: PopulationControl,
  GetMaterialLocations: GetMaterialLocations,
};
