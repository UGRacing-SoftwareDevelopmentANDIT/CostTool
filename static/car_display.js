window.onload = function() {
  // Brakes
  var brakes = document.createElement("img");
  brakes.setAttribute("class", "system_image");
  brakes.setAttribute("src", "{% static 'images/brakes.png' %}");
  brakes.setAttribute("style", "height: 70px; width: 70px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("Brakes").appendChild(brakes);

  // Engine and Drivetrain
  var engine_and_drivetrain = document.createElement("img");
  engine_and_drivetrain.setAttribute("class", "system_image");
  engine_and_drivetrain.setAttribute("src", "{% static 'images/engine_and_drivetrain.png' %}");
  engine_and_drivetrain.setAttribute("style", "height: 70px; width: 70px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("E & Drivetrain").appendChild(engine_and_drivetrain);

  // Frame and <body>
  var frame_and_body = document.createElement("img");
  frame_and_body.setAttribute("class", "system_image");
  frame_and_body.setAttribute("src", "{% static 'images/frame_and_body.png' %}");
  frame_and_body.setAttribute("style", "height: 46px; width: 140px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("Frame & Body").appendChild(frame_and_body);

  // Electrical
  var electrical = document.createElement("img");
  electrical.setAttribute("class", "system_image");
  electrical.setAttribute("src", "{% static 'images/electrical.png' %}");
  electrical.setAttribute("style", "height: 70px; width: 70px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("Electrical").appendChild(electrical);

  // Miscellaneous, Fit, Finish & Assembly
  var misc = document.createElement("img");
  misc.setAttribute("class", "system_image");
  misc.setAttribute("src", "{% static 'images/misc.png' %}");
  misc.setAttribute("style", "height: 70px; width: 26px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("Miscellaneous").appendChild(misc);

  // Steering System
  var steering = document.createElement("img");
  steering.setAttribute("class", "system_image");
  steering.setAttribute("src", "{% static 'images/steering.png' %}");
  steering.setAttribute("style", "height: 70px; width: 70px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("Steering System").appendChild(steering);

  // Suspension System
  var suspension = document.createElement("img");
  suspension.setAttribute("class", "system_image");
  suspension.setAttribute("src", "{% static 'images/suspension.png' %}");
  suspension.setAttribute("style", "height: 70px; width: 70px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("Suspension").appendChild(suspension);

  // Wheels, Wheel  Bearings & Tyres
  var wheels = document.createElement("img");
  wheels.setAttribute("class", "system_image");
  wheels.setAttribute("src", "{% static 'images/wheels.png' %}");
  wheels.setAttribute("style", "height: 55px; width: 70px; display: block; margin-left: auto; margin-right: auto;");
  document.getElementById("Wheels & Tyres").appendChild(wheels);
}
