# Monte Carlo Option Pricing

## Description

This project implements a Monte Carlo simulation for option pricing, leveraging numba for dynamic compilation and performance enhancement. The primary objective is to estimate the value of an option based on the Monte Carlo method, which utilizes random sampling to compute the results.

## Features
**Monte Carlo Simulation:** Simulates numerous paths of stock prices to estimate the option value.

**Dynamic Compilation with Numba:** Uses Numba's @jit decorator to dynamically compile the simulation function, improving performance by optimizing execution speed.

**Flexible Contract Selection:** Enables users to choose exactly which option they want to value. 

https://github.com/user-attachments/assets/030548fb-002e-495e-a012-ec3e72d2186e

| Technologies Used  | Uses |
| ------------- | ------------- |
| yfinance  | Library used to retrieve real-time stock data and option contract offerings |
| numpy  | Manages arrays for the Monte Carlo Simulation  |
| pandas  | Used for managing live stock data |
| datetime  | Module used to calcuate time horizon for options  |
| numba  | Used to dynamically-compile the simulation   |
| tabulate  | Used for presenting option choices to user  |








