# SML Professional Mobile App - Developer Quick Start Guide

## 🚀 Quick Setup

### Prerequisites
- **Flutter SDK**: 3.16.0 or higher
- **Dart SDK**: 3.2.0 or higher
- **Android Studio** / **VS Code** with Flutter extensions
- **Android Emulator** or **Physical Device**
- **Git** for version control

### 1. Clone and Setup
```bash
# Clone the repository
git clone <your-repo-url>
cd mobile_app

# Install dependencies
flutter pub get

# Run the app
flutter run
```

### 2. Environment Configuration
Create a `.env` file in the root directory:
```env
# API Configuration
API_BASE_URL=http://your-django-api-url.com
API_TIMEOUT=30000

# App Configuration
APP_NAME=SML Professional
APP_VERSION=1.0.0
ENVIRONMENT=development

# Feature Flags
ENABLE_BIOMETRIC=true
ENABLE_OFFLINE_MODE=true
ENABLE_PUSH_NOTIFICATIONS=true
```

## 🏗️ Project Structure

```
mobile_app/
├── lib/
│   ├── config/           # App configuration
│   ├── models/           # Data models
│   ├── providers/        # State management
│   ├── screens/          # UI screens
│   ├── services/         # API services
│   ├── utils/            # Utilities and constants
│   ├── widgets/          # Reusable widgets
│   └── main.dart         # App entry point
├── assets/               # Images, fonts, etc.
├── test/                 # Test files
└── pubspec.yaml          # Dependencies
```

## 🔧 Key Components

### 1. State Management (Provider Pattern)
```dart
// Access providers
final clientProvider = context.read<SMLClientProvider>();
final loanProvider = context.read<SMLLoanProvider>();

// Listen to changes
Consumer<SMLClientProvider>(
  builder: (context, provider, child) {
    return Text('${provider.clients.length} clients');
  },
)
```

### 2. API Integration
```dart
// Use SML API service
final apiService = SMLApiService();

// Fetch clients
final clients = await apiService.getSMLClients(
  page: 1,
  pageSize: 20,
  search: 'John',
);
```

### 3. Navigation (GetX)
```dart
// Navigate to screens
Get.toNamed('/client-details', arguments: client);
Get.back();
Get.offAllNamed('/dashboard');
```

## 📱 Running the App

### Development Mode
```bash
# Run with hot reload
flutter run

# Run on specific device
flutter run -d <device-id>

# Run with specific flavor
flutter run --flavor development
```

### Production Build
```bash
# Build APK
flutter build apk --release

# Build App Bundle
flutter build appbundle --release

# Build for specific platform
flutter build apk --target-platform android-arm64
```

## 🧪 Testing

### Run Tests
```bash
# Run all tests
flutter test

# Run specific test file
flutter test test/widget_test.dart

# Run with coverage
flutter test --coverage
```

### Test Structure
```
test/
├── unit/                 # Unit tests
├── widget/               # Widget tests
├── integration/          # Integration tests
└── mocks/               # Mock data
```

## 🔌 API Integration

### Backend Requirements
- **Django REST Framework** with JWT authentication
- **CORS** enabled for mobile app
- **SML-specific endpoints** implemented
- **File upload** support for documents

### API Endpoints
```dart
// Base URL configuration
static const String apiBaseUrl = 'http://your-api.com/api';

// Available endpoints
'/sml-clients/'           // Client management
'/sml-loans/'            // Loan management
'/sml-field-visits/'     // Field operations
'/sml-kyc-documents/'    // Document management
'/dashboard/stats/'      // Dashboard analytics
'/analytics/'            // Business analytics
'/reports/'              // Report generation
'/search/'               // Global search
'/sync/'                 // Offline sync
```

## 🎨 UI Development

### Theme System
```dart
// Access theme
final theme = Theme.of(context);
final colors = AppTheme.primaryColor;

// Use custom styles
Text('Hello', style: AppTheme.headingStyle);
```

### Custom Widgets
```dart
// Use custom components
CustomButton(
  text: 'Submit',
  onPressed: () => _handleSubmit(),
  style: ButtonStyle.primary,
);

CustomTextField(
  hintText: 'Enter name',
  validator: (value) => value?.isEmpty == true ? 'Required' : null,
);
```

## 📊 Data Models

### SML Models
```dart
// Client model
SMLClient client = SMLClient(
  id: 1,
  clientCode: 'CL001',
  firstName: 'John',
  lastName: 'Doe',
  phoneNumber: '+1234567890',
  // ... other fields
);

// Loan model
SMLLoanApplication loan = SMLLoanApplication(
  id: 1,
  loanCode: 'LN001',
  clientId: 1,
  loanAmount: 50000.0,
  interestRate: 12.5,
  // ... other fields
);
```

## 🔐 Authentication

### Login Flow
```dart
// Authenticate user
final authProvider = context.read<AuthProvider>();
await authProvider.login(username, password);

// Check authentication status
if (authProvider.isAuthenticated) {
  // Navigate to dashboard
  Get.offAllNamed('/dashboard');
}
```

### Biometric Setup
```dart
// Setup biometric authentication
final authProvider = context.read<AuthProvider>();
await authProvider.setupBiometric();

// Use biometric login
await authProvider.loginWithBiometric();
```

## 📱 Platform Specific

### Android
```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<uses-permission android:name="android.permission.INTERNET" />
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

### iOS
```xml
<!-- ios/Runner/Info.plist -->
<key>NSCameraUsageDescription</key>
<string>Camera access for document scanning</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>Location access for field visits</string>
```

## 🚨 Common Issues & Solutions

### 1. Build Errors
```bash
# Clean and rebuild
flutter clean
flutter pub get
flutter run
```

### 2. API Connection Issues
- Check API base URL in `app_config.dart`
- Verify backend server is running
- Check CORS configuration
- Verify authentication tokens

### 3. State Management Issues
- Ensure providers are properly registered in `main.dart`
- Check provider lifecycle management
- Verify data flow between providers

### 4. UI Rendering Issues
- Check theme configuration
- Verify widget tree structure
- Check for null safety issues

## 📚 Additional Resources

### Documentation
- [Flutter Documentation](https://flutter.dev/docs)
- [Provider Package](https://pub.dev/packages/provider)
- [GetX Documentation](https://pub.dev/packages/get)
- [Dio HTTP Client](https://pub.dev/packages/dio)

### Code Examples
- Check `example/` directory for usage examples
- Review existing screen implementations
- Study provider patterns in existing code

### Support
- Check GitHub issues for known problems
- Review implementation status document
- Contact development team for assistance

## 🎯 Next Steps

1. **Complete Core Screens**: Finish enhanced loans, field operations, and reports screens
2. **Implement Advanced Features**: Add QR scanning, document management, offline support
3. **Testing**: Implement comprehensive test suite
4. **Performance Optimization**: Optimize app performance and memory usage
5. **Security Hardening**: Implement additional security measures
6. **Deployment**: Prepare for app store submission

---

*Happy Coding! 🚀*
*For questions or support, contact the development team.*

