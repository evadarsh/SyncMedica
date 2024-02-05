// ignore_for_file: unused_import

import 'package:flutter/material.dart';
import 'package:sync_medica/signup_page.dart';
import 'package:sync_medica/forgotpassword_page.dart';
import 'package:sync_medica/home_page.dart';

class LoginPage extends StatelessWidget {
  const LoginPage({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: Scaffold(
        body: Container(
          margin: const EdgeInsets.all(24),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.spaceEvenly,
            children: [
              _header(context),
              _inputField(context),
              _forgotPassword(context),
              _signup(context),
            ],
          ),
        ),
      ),
    );
  }

  _header(context) {
    return Column(
      children: [
        const SizedBox(height: 50),
        const Image(
          image: AssetImage('assets/logo2.png'),
          height: 100, 
          width: 100, 
        ),
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
        )
      ],
    );
  }

  _inputField(context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.stretch,
      children: [
        TextField(
          decoration: InputDecoration(
              hintText: "Email",
              border: OutlineInputBorder(
                  borderRadius: BorderRadius.circular(18),
                  borderSide: BorderSide.none),
              fillColor: const Color.fromARGB(255, 0, 188, 176).withOpacity(0.1),
              filled: true,
              prefixIcon: const Icon(Icons.person)),
        ),
        const SizedBox(height: 10),
        TextField(
          decoration: InputDecoration(
            hintText: "Password",
            border: OutlineInputBorder(
                borderRadius: BorderRadius.circular(18),
                borderSide: BorderSide.none),
            fillColor: const Color.fromARGB(255, 0, 188, 176).withOpacity(0.1),
            filled: true,
            prefixIcon: const Icon(Icons.key_outlined),
          ),
          obscureText: true,
        ),
        const SizedBox(height: 10),
        ElevatedButton(
          onPressed: () {
            Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const HomePage()),
        );
          },
          style: ElevatedButton.styleFrom(
            shape: const StadiumBorder(),
            padding: const EdgeInsets.symmetric(vertical: 16),
            backgroundColor: const Color.fromARGB(255, 0, 188, 176),
          ),
          child: const Text(
            "Login",
            style: TextStyle(
                fontSize: 20, color: Color.fromARGB(255, 255, 255, 255)),
          ),
        )
      ],
    );
  }

  _forgotPassword(context) {
    return TextButton(
      onPressed: () {
        Navigator.push(
          context,
          MaterialPageRoute(builder: (context) => const ForgotPasswordPage()),
        );
      },
      child: const Text(
        "Forgot password?",
        style: TextStyle(color: Color.fromARGB(255, 0, 194, 234)),
      ),
    );
  }

  _signup(context) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        const Text("Don't have an account? "),
        TextButton(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const SignupPage()),
              );
            },
            child: const Text(
              "Sign Up",
              style: TextStyle(color: Color.fromARGB(255, 0, 188, 176)),
            ))
      ],
    );
  }
}
