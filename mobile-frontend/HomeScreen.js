import { View, Text, Button } from 'react-native';

export default function HomeScreen({ navigation }) {

  const checkBackend = async () => {
    try {
      const response = await fetch(
        'http://10.138.145.131:8000/health'
      );
      const data = await response.json();
      alert('Backend connected: ' + JSON.stringify(data));
    } catch (error) {
      alert('Backend NOT reachable');
      console.log(error);
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
      <Text>Civic Issue App</Text>

     

      <Button
        title="Report Issue"
        onPress={() => navigation.navigate('Camera')}
      />
    </View>
  );
}
