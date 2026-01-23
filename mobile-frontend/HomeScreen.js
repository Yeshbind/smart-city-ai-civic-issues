import { View, Text, Button } from 'react-native';

export default function HomeScreen({ navigation }) {
  return (
    <View
      style={{
        flex: 1,
        justifyContent: 'center',
        alignItems: 'center',
        padding: 20,
      }}
    >
      <Text style={{ fontSize: 26, marginBottom: 20 }}>
        Civic Issue App
      </Text>

      <Button
        title="Report Issue"
        onPress={() => navigation.navigate('Camera')}
      />
    </View>
  );
}
