import 'package:flutter/material.dart';
import 'package:sync_medica/login_page.dart';

class ForgotPasswordPage extends StatelessWidget {
  const ForgotPasswordPage({Key? key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          children: [
            const SizedBox(height: 50),
            const Image(
              image: AssetImage('assets/logo2.png'),
              height: 150, 
              width: 150, 
            ),
            const SizedBox(height: 30),
            RichText(
              text: const TextSpan(
                children: [
                  TextSpan(
                    text: "Sync",
                    style: TextStyle(
                      fontSize: 45,
                      fontWeight: FontWeight.bold,
                      color: Color.fromARGB(255, 0, 194, 234),
                    ),
                  ),
                  TextSpan(
                    text: " Medica",
                    style: TextStyle(
                      fontSize: 45,
                      fontWeight: FontWeight.bold,
                      color: Color.fromARGB(255, 0, 188, 176),
                    ),
                  ),
                ],
              ),
            ),
            const SizedBox(height: 20),
            const Text(
              'Enter your email to reset password',
              style: TextStyle(fontSize: 18, color: Color.fromARGB(255, 80, 79, 79)),
            ),
            const SizedBox(height: 20),
            _buildEmailField(),
            const SizedBox(height: 20),
            _buildResetButton(context),
          ],
        ),
      ),
    );
  }

  Widget _buildEmailField() {
    return TextField(
      keyboardType: TextInputType.emailAddress,
      decoration: InputDecoration(
        hintText: 'Email',
        prefixIcon: const Icon(Icons.email),
        border: OutlineInputBorder(
          borderRadius: BorderRadius.circular(18),
        ),
      ),
    );
  }

  Widget _buildResetButton(BuildContext context) {
    return ElevatedButton(
      onPressed: () {
        // Implement your password reset logic here
        _showResetConfirmationDialog(context);
      },
      style: ElevatedButton.styleFrom(
        shape: const StadiumBorder(),
        padding: const EdgeInsets.symmetric(vertical: 12, horizontal: 26),
        backgroundColor: Color.fromARGB(255, 0, 188, 176), 
      ),
      child: const Text('  Sent Password Reset Link ', style: TextStyle(color: Color.fromARGB(255, 255, 255, 255))),
    );
  }

  Future<void> _showResetConfirmationDialog(BuildContext context) async {
    return showDialog<void>(
      context: context,
      builder: (BuildContext context) {
        return AlertDialog(
          title: const Text('Password Reset'),
          content: const Text('An email with instructions has been sent to your address.'),
          actions: <Widget>[
            TextButton(
            onPressed: () {
              Navigator.of(context).pop(); 
              Navigator.of(context).pushReplacement(
                MaterialPageRoute(builder: (context) => LoginPage()), 
              );
            },
            child: const Text('OK'),
          ),
          ],
        );
      },
    );
  }
}

void main() {
  runApp(const MaterialApp(
    home: ForgotPasswordPage(),
  ));
}
