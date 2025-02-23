# SKB Particle Modeler

A web-based tool for modeling and analyzing particles using the Spacetime Klein Bottle (SKB) framework. This application provides an interactive interface for exploring particle properties through topological features and geometric relationships.

## Overview

The SKB Particle Modeler implements the theoretical framework described in ["A Categorical Framework for Topological Features of Spacetime Klein Bottles in Particle Physics"](https://figshare.com/articles/preprint/A_Categorical_Framework_for_Topological_Features_of_Spacetime_Klein_Bottles_in_Particle_Physics/28466279?file=52550969). It allows users to:

- Model fundamental particles using twist numbers and linking pairs
- Analyze particle properties like charge and mass
- Compare predicted values with actual measurements
- Explore predefined particle configurations
- Create and validate custom particle models

## Features

### Particle Configuration
- Select from predefined particles (proton, neutron, electron)
- Define custom particles using:
  - Twist numbers
  - Linking pairs
  - Custom naming

### Analysis Tools
- Individual particle analysis
- Batch analysis of multiple configurations
- Automated iteration through configurations
- Real-time validation and error reporting

### Mass Parameters
- Configure γ (gamma), δ (delta), and ε (epsilon) parameters
- Automatic parameter fitting
- Parameter validation and updating
- Error percentage calculations

## Usage

1. **Basic Analysis**
   - Select a predefined particle or create a custom configuration
   - Enter twist numbers and linking pairs
   - Click "Analyze Selected" to see results

2. **Mass Parameter Fitting**
   - Use "Fit Parameters" to automatically calculate optimal values
   - Manually adjust parameters as needed
   - Update and validate results in real-time

3. **Batch Processing**
   - Use "Analyze All Particles" for bulk analysis
   - Start automated iteration for sequential processing
   - Review results in the formatted table display

## Interface Structure

The application consists of three main pages:
- **Introduction** (particle_modeler.html): Overview and basic concepts
- **Modeler** (modeler.html): Main configuration interface
- **Analysis** (index.html): Results and parameter management

## Technical Details

### Particle Configuration Format
```javascript
{
    twistNumbers: "2,2,-1",  // Comma-separated integers
    linkingPairs: "0,1,1;1,2,1",  // Semicolon-separated triples
    name: "custom"  // Optional particle name
}
```

### Mass Parameters
- γ (gamma): Mass scale parameter (-10 to 10)
- δ (delta): Mass offset parameter (-10 to 10)
- ε (epsilon): Mass correction parameter (-10 to 10)

## Results Format

Analysis results include:
- Predicted charge
- Actual charge
- Predicted mass
- Actual mass
- Mass error percentage

## Error Handling

The application includes comprehensive error handling for:
- Invalid input validation
- Network request failures
- Parameter range violations
- Configuration format errors

## Styling

The interface uses a consistent design system with:
- Card-based layout
- Info boxes for guidance
- Clear status indicators
- Responsive controls
- Accessible form elements

## Requirements

- Modern web browser with JavaScript enabled
- Server capable of handling HTTP requests
- CSS3 support for styling