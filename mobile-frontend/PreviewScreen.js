import { View, Image, Button, Alert } from 'react-native';

export default function PreviewScreen({ route, navigation }) {
  const { image } = route.params;

  const submitIssue = async () => {
    try {
      const formData = new FormData();

      formData.append('file', {
        uri: image,
        name: 'violation.jpg',
        type: 'image/jpeg',
      });

      const response = await fetch(
        'http://10.138.145.131:8000/api/detect-violation',
        {
          method: 'POST',
          body: formData,
      
        }
      );

      const result = await response.json();

      if (result.status === 'success') {
        Alert.alert('Success', result.message || 'Violation detected');
      } else {
        Alert.alert('Result', result.message || 'No violation detected');
      }

      navigation.navigate('Home');
    } catch (error) {
      console.log(error);
      Alert.alert('Error', 'Failed to connect to backend');
    }
  };

  return (
    <View style={{ flex: 1 }}>
      <Image source={{ uri: image }} style={{ flex: 1 }} />
      <Button title="Submit Issue" onPress={submitIssue} />
    </View>
  );
}
