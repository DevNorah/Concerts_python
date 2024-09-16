# Concert Management System

The **Concert Management System** is a Python application that uses SQLite to manage data related to concerts, bands, and venues. The system provides an interface for storing and retrieving information about bands, venues, and concerts, along with several utility methods to help manage the relationships between these entities.

## Features

- **Bands**: Store information about bands such as name and hometown.
- **Venues**: Store information about venues including title and city.
- **Concerts**: Manage concerts by linking bands and venues along with their scheduled dates.
- Retrieve details about concerts, bands, and venues.
- Support methods for querying concerts, venues, and bands (e.g., find the most frequent band in a venue, or check if a concert is a "hometown" show).

## Table of Contents

- [Setup](#setup)
- [Database Schema](#database-schema)
- [Classes and Methods](#classes-and-methods)
- [Usage](#usage)
- [License](#license)

## Setup

### Prerequisites

- Python 3.x installed on your system.
- SQLite3 (should come pre-installed with Python).

### Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/https://github.com/DevNorah/Concerts_python

2. Navigate to the project directory:

    ```bash
    cd concerts

3. Ensure all dependencies are installed (SQLite is required, which is included with Python by default).

### Database Schema
The database contains three main tables:

1. Bands:

- id: Primary key (integer).
- name: Name of the band (text, required).
- hometown: Hometown of the band (text, required).

2. Venues:

- id: Primary key (integer).
- title: Name of the venue (text, required).
- city: City where the venue is located (text, required).

3. Concerts:

- id: Primary key (integer).
- band_id: Foreign key linking to the bands table.
- venue_id: Foreign key linking to the venues table.
- date: Date of the concert (text, required).

## Classes and Methods

### Concert Class

The Concert class handles interactions related to concerts.

- band(concert_id): Returns the band details for the given concert.

- venue(concert_id): Returns the venue details for the given concert.

- hometown_show(): Returns True if the concert is in the band's hometown, False otherwise.

- introduction(): Returns a string introducing the band and the city of the concert.

### Band Class

The Band class manages bands and their associated concerts.

- concerts(band_id): Returns a list of all concerts for a given band.

- venues(band_id): Returns a list of venues where the band has performed.

- play_in_venue(band_id, venue_id, date): Adds a new concert for the band at a specific venue and date.

- all_introductions(band_id): Returns a list of introduction messages for all concerts by the band.

- most_performances(): Returns the band with the highest number of performances.


### Venue Class

The Venue class manages venues and their concerts.

- concerts(venue_id): Returns a list of concerts happening at a given venue.

- bands(venue_id): Returns a list of bands that have performed at the venue.

- concert_on(venue_id, date): Returns the concert details for a given date at the venue.

- most_frequent_band(venue_id): Returns the band that has performed the most at the venue.

## Usage
After setting up, you can seed the database with some initial data by running:

```bash
    python3 concerts.py
```

Author

Norah Kinyamasyo.