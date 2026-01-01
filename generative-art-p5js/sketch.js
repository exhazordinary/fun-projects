// Flow Field - Generative Art with p5.js

let particles = [];
let flowField;
let cols, rows;
let scale = 20;
let zoff = 0;
let colorMode_idx = 0;

const PARTICLE_COUNT = 1000;

function setup() {
  createCanvas(windowWidth, windowHeight);
  colorMode(HSB, 360, 100, 100, 100);
  background(0);

  cols = floor(width / scale);
  rows = floor(height / scale);
  flowField = new Array(cols * rows);

  for (let i = 0; i < PARTICLE_COUNT; i++) {
    particles.push(new Particle());
  }
}

function draw() {
  // Update flow field with Perlin noise
  let yoff = 0;
  for (let y = 0; y < rows; y++) {
    let xoff = 0;
    for (let x = 0; x < cols; x++) {
      let index = x + y * cols;
      let angle = noise(xoff, yoff, zoff) * TWO_PI * 2;
      let v = p5.Vector.fromAngle(angle);
      v.setMag(1);
      flowField[index] = v;
      xoff += 0.1;
    }
    yoff += 0.1;
  }
  zoff += 0.003;

  // Update and draw particles
  for (let particle of particles) {
    particle.follow(flowField);
    particle.update();
    particle.edges();
    particle.show();
  }
}

class Particle {
  constructor() {
    this.pos = createVector(random(width), random(height));
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
    this.maxSpeed = 4;
    this.prevPos = this.pos.copy();
    this.hue = random(360);
  }

  follow(vectors) {
    let x = floor(this.pos.x / scale);
    let y = floor(this.pos.y / scale);
    let index = x + y * cols;
    let force = vectors[index];
    if (force) {
      this.applyForce(force);
    }
  }

  applyForce(force) {
    this.acc.add(force);
  }

  update() {
    this.vel.add(this.acc);
    this.vel.limit(this.maxSpeed);
    this.pos.add(this.vel);
    this.acc.mult(0);
  }

  edges() {
    if (this.pos.x > width) {
      this.pos.x = 0;
      this.updatePrev();
    }
    if (this.pos.x < 0) {
      this.pos.x = width;
      this.updatePrev();
    }
    if (this.pos.y > height) {
      this.pos.y = 0;
      this.updatePrev();
    }
    if (this.pos.y < 0) {
      this.pos.y = height;
      this.updatePrev();
    }
  }

  updatePrev() {
    this.prevPos.x = this.pos.x;
    this.prevPos.y = this.pos.y;
  }

  show() {
    let col = getColor(this.pos, this.hue);
    stroke(col);
    strokeWeight(1);
    line(this.pos.x, this.pos.y, this.prevPos.x, this.prevPos.y);
    this.updatePrev();
  }
}

function getColor(pos, baseHue) {
  switch (colorMode_idx) {
    case 0: // Rainbow based on position
      return color((pos.x + pos.y) * 0.2 % 360, 80, 90, 5);
    case 1: // Ocean blues
      return color(200 + noise(pos.x * 0.01, pos.y * 0.01) * 40, 70, 80, 5);
    case 2: // Fire
      return color(noise(pos.x * 0.01) * 60, 90, 90, 5);
    case 3: // Monochrome
      return color(0, 0, 90, 3);
    default:
      return color(baseHue, 70, 80, 5);
  }
}

function keyPressed() {
  if (key === ' ') {
    background(0);
    for (let particle of particles) {
      particle.pos = createVector(random(width), random(height));
      particle.updatePrev();
    }
  }
  if (key === '1') colorMode_idx = 0;
  if (key === '2') colorMode_idx = 1;
  if (key === '3') colorMode_idx = 2;
  if (key === '4') colorMode_idx = 3;
  if (key === '+' || key === '=') {
    for (let i = 0; i < 100; i++) {
      particles.push(new Particle());
    }
  }
  if (key === '-') {
    particles.splice(0, min(100, particles.length));
  }
}

function windowResized() {
  resizeCanvas(windowWidth, windowHeight);
  cols = floor(width / scale);
  rows = floor(height / scale);
  flowField = new Array(cols * rows);
  background(0);
}
