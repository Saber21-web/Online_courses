if (Notification.permission === 'granted') {
    new Notification('Уведомление', {
      body: 'Это тестовое уведомление',
      icon: 'icon.png'
    });
  } else if (Notification.permission !== 'denied') {
    Notification.requestPermission().then(function (permission) {
      // Если разрешение получено, создать уведомление
    });
  }