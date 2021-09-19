# Compass simulator

A Python package to make balance, stability and rapidity simulations of an orienteering compass.

<!-- TABLE OF CONTENTS -->
## Table of Contents

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
    <li><a href="#usage">Usage</a></li>
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

1. Clone the repo
```sh
git clone https://github.com/NicoRio42/compass-simulator.git
```
2. pip
```sh
pip install requirements.txt
```


<!-- USAGE EXAMPLES -->
## Usage

Use this space to show useful examples of how a project can be used. Additional screenshots, code examples and demos work well in this space. You may also link to more resources.


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


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/NicoRio42/repo.svg?style=for-the-badge
[contributors-url]: https://github.com/NicoRio42/compass-simulator/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/NicoRio42/repo.svg?style=for-the-badge
[forks-url]: https://github.com/NicoRio42/compass-simulator/network/members
[stars-shield]: https://img.shields.io/github/stars/NicoRio42/repo.svg?style=for-the-badge
[stars-url]: https://github.com/NicoRio42/compass-simulator/stargazers
[issues-shield]: https://img.shields.io/github/issues/NicoRio42/repo.svg?style=for-the-badge
[issues-url]: https://github.com/NicoRio42/compass-simulator/issues
[license-shield]: https://img.shields.io/github/license/NicoRio42/repo.svg?style=for-the-badge
[license-url]: https://github.com/NicoRio42/compass-simulator/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://linkedin.com/in/NicoRio42
