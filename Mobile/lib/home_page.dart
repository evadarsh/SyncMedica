import 'package:flutter/material.dart';

class HomePage extends StatelessWidget {
  const HomePage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        automaticallyImplyLeading: false, 
        title: SizedBox(
          height: kToolbarHeight,
          child: Image.asset(
            'assets/logo.png',
            fit: BoxFit.contain,
          ),
        ),
        backgroundColor: const Color.fromARGB(255, 255, 255, 255),
        actions: [
          IconButton(
            icon: const Icon(Icons.account_circle),
            onPressed: () {
              
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => ProfilePage()),
              );
            },
          ),
        ],
      ),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'assets/logo2.png', // Replace with your own doctor icon image
              height: 150,
            ),
            const SizedBox(height: 20),
            const SizedBox(height: 20),
            ElevatedButton(
              onPressed: () {
                // Navigate to the doctor list page
                Navigator.push(
                  context,
                  MaterialPageRoute(builder: (context) => DoctorListPage()),
                );
              },
              child: const Text('Find a Doctor'),
            ),
          ],
        ),
      ),
    );
  }
}

class DoctorListPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Available Doctors'),
        backgroundColor: Colors.blue, // Replace with your desired color
        actions: [
          IconButton(
            icon: const Icon(Icons.account_circle),
            onPressed: () {
              // Navigate to the profile page
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => ProfilePage()),
              );
            },
          ),
        ],
      ),
      body: ListView(
        children: [
          DoctorCard(
              'Dr. John Doe', 'Cardiologist', 'Monday, 9:00 AM - 5:00 PM'),
          DoctorCard('Dr. Jane Smith', 'Dermatologist',
              'Wednesday, 2:00 PM - 8:00 PM'),
          // Add more DoctorCard widgets for other doctors
        ],
      ),
    );
  }
}

class DoctorCard extends StatelessWidget {
  final String name;
  final String specialty;
  final String availability;

  DoctorCard(this.name, this.specialty, this.availability);

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.all(8),
      child: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              name,
              style: const TextStyle(
                fontSize: 18,
                fontWeight: FontWeight.bold,
              ),
            ),
            const SizedBox(height: 8),
            Text(
              'Specialty: $specialty',
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 8),
            Text(
              'Availability: $availability',
              style: const TextStyle(fontSize: 16),
            ),
            const SizedBox(height: 8),
            ElevatedButton(
              onPressed: () {
                // Implement booking functionality here
                // You can navigate to a booking page or show a confirmation dialog
                // For simplicity, we'll just print a message for now
                print('Appointment booked with $name');
              },
              child: const Text('Book Appointment'),
            ),
          ],
        ),
      ),
    );
  }
}

class ProfilePage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('My Profile'),
      ),
      body: const Center(
        child: Text('User Profile'),
      ),
    );
  }
}
