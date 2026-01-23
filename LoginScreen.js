import { View, Text, TextInput, Button } from 'react-native';
import { useState } from 'react';

export default function LoginScreen({ navigation }) {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <View
      style={{
        flex: 1,
        justifyContent: 'center',
        padding: 20,
      }}
    >
      <Text style={{ fontSize: 28, marginBottom: 10 }}>
        Civic Issue App
      </Text>

      <Text style={{ fontSize: 16, marginBottom: 30 }}>
        Field Staff Login
      </Text>

      <TextInput
        placeholder="Email"
        value={email}
        onChangeText={setEmail}
        autoCapitalize="none"
        style={{
          borderWidth: 1,
          padding: 12,
          marginBottom: 15,
          borderRadius: 6,
        }}
      />

      <TextInput
        placeholder="Password"
        value={password}
        onChangeText={setPassword}
        secureTextEntry
        style={{
          borderWidth: 1,
          padding: 12,
          marginBottom: 25,
          borderRadius: 6,
        }}
      />

      <Button
        title="Login"
        onPress={() => navigation.navigate('Home')}
      />
    </View>
  );
}