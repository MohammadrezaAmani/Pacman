# Pacman

**Description:**
    Pacman Solver is an advanced implementation of the classic Pacman game, featuring a fast solver utilizing the Minimax algorithm, Alpha-Beta pruning, and A* heuristic. This project is designed with modularity and object-oriented principles in mind, providing a well-structured and efficient solution.

## Features

- **Minimax Algorithm:** The solver employs the Minimax algorithm to make optimal decisions, ensuring Pacman navigates the maze effectively.

- **Alpha-Beta Pruning:** Optimizes the Minimax algorithm by eliminating suboptimal branches, improving performance without compromising accuracy.

- **A* Heuristic:** Enhances decision-making with the A* heuristic, allowing Pacman to make informed choices based on an efficient cost estimation.

- **Modular Design:** The project is organized using Object-Oriented Programming (OOP) principles, promoting code readability, maintainability, and ease of extension.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MohammadrezaAmani/Pacman.git
   ```

2. Navigate to the project directory:

   ```bash
   cd Pacman
   ```

3. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

   ```python
   python main.py
   ```

This command initiates the Pacman Solver, allowing it to demonstrate its capabilities on a sample Pacman maze.

## Configuration

The solver's behavior can be configured through the following parameters:

- **Depth:** Adjust the depth of the Minimax algorithm by modifying the `DEPTH` variable in the `config.py` file.

- **Heuristic Weight:** Tune the influence of the A* heuristic by modifying the `HEURISTIC_WEIGHT` variable in the `config.py` file.

## Contributing

Contributions are welcome! If you'd like to enhance the project or fix any issues, please follow these steps:

  1. Fork the repository.
  2. Create a new branch (`git checkout -b feature/your-feature`).
  3. Commit your changes (`git commit -m 'Add some feature'`).
  4. Push to the branch (`git push origin feature/your-feature`).
  5. Open a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](./LICENSE) file for details.

## Acknowledgments

- The Pacman Solver project was inspired by the classic Pacman game and various AI algorithms used in game-solving.

## Contact

For any inquiries, please contact [more.amani@yahoo.com](mainto:more.amani@yahoo.com).
