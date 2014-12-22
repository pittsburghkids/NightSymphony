public class Swarm {

  ArrayList<Insect> insects;
  int activeCount = 0;

  Swarm() {

    insects = new ArrayList<Insect>();

    insects.add( new Insect(15, "Symphony_mixdown_Bee_1.wav") );
    //insects.add( new Insect(14, "Symphony_mixdown_Bee_2.wav") );
    insects.add( new Insect(14, "Symphony_mixdown_Cicada_1.wav") );
    //insects.add( new Insect(25, "Symphony_mixdown_Cicada_2.wav") );
    insects.add( new Insect(19, "Symphony_mixdown_Cricket_1.wav") );
    //insects.add( new Insect(27, "Symphony_mixdown_Cricket_2.wav") );
    //insects.add( new Insect(28, "Symphony_mixdown_Cricket_3.wav") );
    //insects.add( new Insect(29, "Symphony_mixdown_Cricket_4.wav") );
    //insects.add( new Insect(30, "Symphony_mixdown_Dragonfly_1.wav") );
    //insects.add( new Insect(31, "Symphony_mixdown_Dragonfly_2.wav") );
    //insects.add( new Insect(32, "Symphony_mixdown_Locust_1.wav") );
    //insects.add( new Insect(33, "Symphony_mixdown_Locust_2.wav") );
    insects.add( new Insect(18, "Symphony_mixdown_Mantis_1.wav") );
    //insects.add( new Insect(35, "Symphony_mixdown_Mantis_2.wav") );
    //insects.add( new Insect(36, "Symphony_mixdown_Mosquito_1.wav") );
    //insects.add( new Insect(37, "Symphony_mixdown_Mosquito_2.wav") );
    insects.add( new Insect(17, "Symphony_mixdown_Spittle_1.wav") );
    //insects.add( new Insect(39, "Symphony_mixdown_Spittle_2.wav") );
    insects.add( new Insect(16, "Symphony_mixdown_Worm_1.wav") );
    //insects.add( new Insect(41, "Symphony_mixdown_Worm_2.wav") );
    //insects.add( new Insect(42, "cricket.wav") );
    //insects.add( new Insect(43, "mantis.wav") );
    //insects.add( new Insect(44, "mosquito.wav") );
    //insects.add( new Insect(45, "spittle.wav") );
  }

  int insectCount() {
    return insects.size();
  }

  Insect getInsect(int index) {
    return insects.get(index);
  }

  void toggleInsect(int index) {
    if (!insects.get(index).awake) {
      wakeInsect(index);
    } else {
      sleepInsect(index);
    }
  }

  void wakeInsect(int index) {
    // Start the clock if it isn't ticking
    if (!clock.ticking) clock.start();

    float offset = clock.getPosition();
    insects.get(index).play(offset);
    activeCount++;
  }

  void sleepInsect(int index) {
    if (insects.get(index).stop()) activeCount--;
  }

  void trigger() {
    for (int i = 0; i < insects.size (); i++) {
      if (insects.get(i).awake) insects.get(i).trigger();
    }
  }
}

