# 🌌 Physics Law Simulations

> Interactive visualizations of fundamental physics laws using Python, Pygame, and NumPy

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.0+-green.svg)](https://www.pygame.org/)
[![NumPy](https://img.shields.io/badge/NumPy-Latest-orange.svg)](https://numpy.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

An educational collection of **19 interactive physics simulations** that bring fundamental laws of physics to life. Each simulation features real-time visualization, interactive controls, and accurate mathematical modeling using NumPy for physics calculations and Pygame for rendering.

---

## 🎯 Features

- **🎮 Interactive Controls**: Manipulate parameters in real-time to see immediate effects
- **📊 Real-time Calculations**: Accurate physics computations using NumPy
- **🎨 Visual Feedback**: Beautiful animations and color-coded elements
- **🌐 Web-Compatible**: Async architecture supports deployment via Pygbag/Emscripten
- **📚 Educational**: Perfect for students, teachers, and physics enthusiasts
- **🏗️ Modular Architecture**: Clean, maintainable code structure

---

## 🚀 Quick Start

### Prerequisites

```bash
pip install pygame numpy
```

### Running a Simulation

```bash
cd Newton-First-Law
python main.py
```

Each simulation is self-contained in its own directory with a `main.py` entry point.

---

## 📖 Simulations

### ⚙️ Classical Mechanics

#### 1️⃣ Newton's First Law (Law of Inertia)
**Formula**: Object maintains velocity unless acted upon by external force

**Interactive Elements**:
- Toggle friction on/off to demonstrate inertia
- Launch ball with random velocity
- Observe motion with and without friction
- Elastic collisions with boundaries

**Controls**: `SPACE` = Launch, `F` = Toggle friction, `S` = Stop, `R` = Reset

---

#### 2️⃣ Newton's Second Law
**Formula**: $F = ma$

**Interactive Elements**:
- Adjust applied force on cart
- Change cart mass dynamically
- Real-time acceleration calculation
- Force and acceleration vectors displayed

**Controls**: `←/→` = Apply force, `Q/W` = Adjust mass

---

#### 3️⃣ Newton's Third Law
**Formula**: For every action, there is an equal and opposite reaction

**Interactive Elements**:
- Two carts collide and exchange momentum
- Action-reaction force pairs visualized
- Adjustable masses and velocities
- Momentum conservation demonstration

**Controls**: `Q/W` = Adjust cart 1 mass, `A/S` = Adjust cart 2 mass, `SPACE` = Launch

---

#### 4️⃣ Law of Universal Gravitation
**Formula**: $F = G \frac{m_1 m_2}{r^2}$

**Interactive Elements**:
- N-body gravitational simulation
- Add/remove celestial bodies
- Adjust masses and see gravitational effects
- Orbital mechanics visualization
- Energy conservation tracking

**Controls**: `Click` = Add body, `Q/W` = Adjust mass, `R` = Reset

---

#### 5️⃣ Conservation of Momentum
**Formula**: $\sum p_{before} = \sum p_{after}$

**Interactive Elements**:
- Elastic and inelastic collision modes
- Real-time momentum calculation
- Multiple cart collisions
- Momentum vector visualization

**Controls**: `SPACE` = Launch, `E/I` = Elastic/Inelastic mode

---

#### 6️⃣ Conservation of Energy
**Formula**: $E_{total} = KE + PE = constant$

**Interactive Elements**:
- Pendulum with energy tracking
- Kinetic and potential energy graphs
- Adjustable length and mass
- Damping and air resistance options
- Energy conservation verification

**Controls**: `Click-Drag` = Set angle, `Q/W` = Length, `A/S` = Mass, `R` = Reset

---

#### 7️⃣ Hooke's Law
**Formula**: $F = -kx$

**Interactive Elements**:
- Spring-mass oscillation system
- Adjustable spring constant (k)
- Mass modification
- Damping control
- Simple harmonic motion demonstration

**Controls**: `Q/W` = Spring constant, `A/S` = Mass, `D` = Toggle damping

---

#### 8️⃣ Archimedes' Principle
**Formula**: $F_{buoyant} = \rho_{fluid} \cdot V_{displaced} \cdot g$

**Interactive Elements**:
- Objects with different densities
- Fluid density adjustment
- Real-time buoyancy force calculation
- Floating, sinking, and neutral buoyancy

**Controls**: `Q/W` = Object density, `A/S` = Fluid density, `SPACE` = Drop object

---

#### 9️⃣ Bernoulli's Principle
**Formula**: $P + \frac{1}{2}\rho v^2 + \rho gh = constant$

**Interactive Elements**:
- Fluid flow through varying pipe diameters
- Pressure and velocity visualization
- Streamline particles
- Venturi effect demonstration

**Controls**: `Q/W` = Flow rate, `A/S` = Pipe diameter

---

### 🔥 Thermodynamics

#### 🌡️ First Law of Thermodynamics
**Formula**: $\Delta U = Q - W$

**Interactive Elements**:
- Ideal gas in piston system
- Heat addition/removal
- Work done by/on gas
- Temperature, pressure, volume tracking
- PV diagram visualization

**Controls**: `Q/W` = Add/remove heat, `A/S` = Compress/expand, `R` = Reset

---

#### 📈 Second Law of Thermodynamics
**Formula**: $\Delta S \geq 0$ (entropy increases)

**Interactive Elements**:
- Heat flow between hot and cold reservoirs
- Entropy calculation and visualization
- Temperature gradient display
- Irreversible process demonstration

**Controls**: `SPACE` = Start heat flow, `R` = Reset

---

### ⚡ Electromagnetism

#### 🔌 Coulomb's Law
**Formula**: $F = k \frac{q_1 q_2}{r^2}$

**Interactive Elements**:
- Multiple point charges (positive and negative)
- Electric force vectors
- Real-time force calculations
- Charge interaction visualization

**Controls**: `Click` = Add charge, `+/-` = Toggle charge sign, `Q/W` = Adjust magnitude

---

#### 🌐 Gauss's Law for Electricity
**Formula**: $\Phi_E = \frac{Q_{enclosed}}{\epsilon_0}$

**Interactive Elements**:
- Electric field line visualization
- Gaussian surface around charges
- Flux calculation through surface
- Field strength color mapping

**Controls**: `Click` = Add charge, `SPACE` = Toggle field lines, `G` = Toggle Gaussian surface

---

#### 🧲 Gauss's Law for Magnetism
**Formula**: $\Phi_B = 0$ (no magnetic monopoles)

**Interactive Elements**:
- Magnetic dipole field visualization
- Closed field lines demonstration
- Gaussian surface with zero net flux
- Bar magnet simulation

**Controls**: `Click-Drag` = Move magnet, `R` = Rotate, `F` = Toggle field lines

---

#### ⚡ Faraday's Law of Induction
**Formula**: $\mathcal{E} = -\frac{d\Phi_B}{dt}$

**Interactive Elements**:
- Moving magnet through coil
- Induced current visualization
- Magnetic flux change display
- EMF meter
- Lenz's law demonstration

**Controls**: `Click-Drag` = Move magnet, `Q/W` = Adjust velocity, `SPACE` = Drop

---

#### 🔄 Ampère's Law
**Formula**: $\oint \vec{B} \cdot d\vec{l} = \mu_0 I_{enclosed}$

**Interactive Elements**:
- Current-carrying wire
- Circular magnetic field lines
- Amperian loop visualization
- Field strength vs. distance

**Controls**: `Q/W` = Adjust current, `A/S` = Loop radius, `SPACE` = Toggle field

---

### 🌊 Quantum & Modern Physics

#### 🎲 Heisenberg's Uncertainty Principle
**Formula**: $\Delta x \cdot \Delta p \geq \frac{\hbar}{2}$

**Interactive Elements**:
- Position and momentum space wave functions
- Gaussian wave packet visualization
- Uncertainty product calculation
- Quantum measurement simulation
- Real-time verification of uncertainty relation

**Controls**: `Q/W` = Adjust Δx, `A/S` = Adjust Δp, `SPACE` = Measure position, `M` = Measure momentum, `C` = Clear measurements

---

#### 💡 Planck's Law
**Formula**: $E = h\nu$

**Interactive Elements**:
- Photon energy vs. frequency
- Electromagnetic spectrum visualization
- Wavelength and frequency adjustment
- Color representation of visible light
- Blackbody radiation

**Controls**: `Q/W` = Adjust frequency, `SPACE` = Emit photon, `R` = Reset

---

#### ⚛️ Einstein's Mass-Energy Equivalence
**Formula**: $E = mc^2$

**Interactive Elements**:
- Three modes: Rest mass, Kinetic energy, Mass-to-energy conversion
- Lorentz factor calculation (special relativity)
- Relativistic mass increase visualization
- Animated particle-to-photon conversion
- Energy conservation demonstration

**Controls**: `1/2/3` = Switch mode, `Q/W` = Adjust mass, `A/S` = Adjust velocity, `SPACE` = Convert to energy

---

## 🏗️ Project Structure

Each simulation follows a consistent, modular architecture:

```
Simulation-Name/
├── __init__.py
├── main.py                  # Entry point with async loop
├── config.py                # Physical constants and parameters
├── physics_*.py             # Physics object classes with NumPy
├── simulation_engine.py     # Game loop (60 FPS)
├── renderer.py              # Pygame visualization
└── input_handler.py         # User input processing
```

### Key Design Principles:
- **Separation of Concerns**: Physics, rendering, and input are decoupled
- **NumPy for Physics**: Efficient vector/matrix operations
- **60 FPS Game Loop**: Smooth animations via async architecture
- **Configurable Parameters**: Easy to adjust via `config.py`

---

## 🛠️ Technical Stack

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Physics Engine** | NumPy | Vector math, numerical integration |
| **Graphics** | Pygame | 2D rendering, event handling |
| **Language** | Python 3.8+ | Main implementation |
| **Async Support** | asyncio | Web deployment compatibility |

---

## 🎓 Educational Use

This project is ideal for:
- 📚 **Physics Students**: Visual understanding of abstract concepts
- 👨‍🏫 **Teachers**: Interactive classroom demonstrations
- 🔬 **Researchers**: Quick prototyping of physics scenarios
- 💻 **Developers**: Learning physics simulation techniques

---

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new physics simulations
- Improve existing visualizations
- Fix bugs or optimize code
- Enhance documentation

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🙏 Acknowledgments

Built with passion for physics and education. Special thanks to the Python, Pygame, and NumPy communities.

---

## 📞 Contact

For questions, suggestions, or collaboration:
- Open an issue on GitHub
- Submit a pull request

---

**⭐ Star this repo if you find it helpful!**
