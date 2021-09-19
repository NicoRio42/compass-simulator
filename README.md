# Compass simulator

A Python package to make balance, stability and rapidity simulations of an orienteering compass.

## Table of Contents
<!-- TABLE OF CONTENTS -->
<details open="open">
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Exemple usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

I wrote this package when I was working at [DECATHLON - GEONAUTE](https://www.decathlon.fr/sport/c0-tous-les-sports/c1-course-d-orientation/_/N-13kthf7) on the improvement of orienteering compasses, as a Research and Development Engineer.

The goal of the project was to model the dynamic behavior of an orienteering compass. Specifically, I was working on the balance, the stability and the rapidity of the needle.

For more on the concepts of balance, stability and rapidity of orienteeering compasses, you can read these two blog posts (in French):
- [How does a compass work? - part 1](https://interpost.fr/article?id=19)
- [How does a compass work? - part 2](https://interpost.fr/article?id=27)

This Research and Development work was notably done for the design of the [R900 GEONAUTE compass](https://www.decathlon.fr/p/boussole-pouce-gauche-pour-course-d-orientation-racer-900-noir/_/R-p-313026?mc=8576047), the high-end product of GEONAUTE's range.

### Built With

* [NumPy](https://numpy.org/)
* [SciPy](https://scipy.org/)
* [Matplotlib](https://matplotlib.org/)


<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

Upgrade pip
```sh
pip install --upgrade pip
```
Download virtualenv
```sh
pip install virtualenv --upgrade
```
Set up a virtual environment
```sh
python -m virtualenv env
```
Activate the virtual environment
```sh
env\Scripts\activate.bat
```

### Installation

Clone the repo
```sh
git clone https://github.com/NicoRio42/compass-simulator.git
```
Install the requirements
```sh
pip install requirements.txt
```


<!-- USAGE EXAMPLES -->
## Exemple usage

Create Compass, and MagneticField objects with default parameters.
```py
from compass_simulator.core import Compass, MagneticField

comp = Compass()
mag_fld = MagneticField()
```

Create a Dynamic object with default parameters for dynamic simulations.
```py
from compass_simulator.core import Dynamic

dyn = Dynamic(comp, mag_fld)
```

Run the stability simulation, and display the result graph.
```py
dyn.stability()
dyn.display_stab()
```

<!-- ROADMAP -->
## Roadmap

See the [open issues](https://github.com/NicoRio42/compass-simulator/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.



<!-- CONTACT -->
## Contact

Nicolas Rio - nicolas.rio42@gmail.com

Project Link: [https://github.com/NicoRio42/compass-simulator](https://github.com/NicoRio42/compass-simulator)