from sequencer.model import Model, bpm_to_seconds_per_beat
import unittest
import time

# time each async test will take in seconsd
TIME_FOR_ASYNC_TESTS = 4.0


class Tests(unittest.TestCase):

    def test_bpm_to_seconds_per_beat(self):
        self.assertAlmostEqual(1.0, bpm_to_seconds_per_beat(60.0), delta=.01)
        self.assertAlmostEqual(.5, bpm_to_seconds_per_beat(120.0), delta=.01)
        self.assertAlmostEqual(2.0/3.0, bpm_to_seconds_per_beat(90.0), delta=.01)

    def test_toggle(self):
        model = Model(8, 8, 120.0, 0.0, 1)
        result = model.toggle_button((0,0))
        self.assertTrue(result)
        self.assertTrue(model.buttons[0][0])

    def test_get_sample_states(self):
        model = Model(8, 8, 120.0, 0.0, 1)
        for sample in range(4, 8):
            model.toggle_button((3, sample))
        states = model.get_sample_states_for_beat(3)
        self.assertEquals(set([False]), set(states[0:4]))
        self.assertEquals(set([True]), set(states[4:]))
        states = model.get_sample_states_for_beat(0)
        self.assertEquals(set([False]), set(states))

    def test_set_number_beats_increase(self):
        model = Model(8, 8, 120.0, 0.0, 1)
        model.set_number_beats(10)
        self.assertTrue(model.number_beats == 10)
        for beat in range(10):
            for sample in range(8):
                position = (beat, sample)
                self.assertFalse(model.buttons[beat][sample])

    def test_set_number_beats_decrease(self):
        model = Model(8, 8, 120.0, 0.0, 1)
        model.set_number_beats(4)
        self.assertTrue(model.number_beats == 4)
        for beat in range(4):
            for sample in range(8):
                position = (beat, sample)
                self.assertFalse(model.buttons[beat][sample])

    def test_set_number_beats_keep_button_states(self):
        model = Model(8, 8, 120.0, 0.0, 1)
        for sample in range(4, 8):
            model.toggle_button((3, sample))
        model.set_number_beats(10)
        states = model.get_sample_states_for_beat(3)
        self.assertEquals(set([False]), set(states[0:4]))
        self.assertEquals(set([True]), set(states[4:]))

    def test_playback_timing_constant_bpm(self):
        print 'this playback timing test takes ~', TIME_FOR_ASYNC_TESTS, 'seconds'
        timing_tolerance = 0.1
        bpm = 240.0
        model = Model(8, 8, bpm, 0.0, 1)
        expected_beat_duration = model._calculate_beat_duration()
        step_times = []
        def assertion_callback(value):
            step_times.append(time.time())

        model.current_beat.add_callback(assertion_callback)
        new_state = model.toggle_playback()
        self.assertTrue(new_state)
        time.sleep(TIME_FOR_ASYNC_TESTS)
        new_state = model.toggle_playback()
        self.assertFalse(new_state)

        for i in range(len(step_times) - 1):
            former = step_times[i]
            latter = step_times[i + 1]
            duration = latter - former
            self.assertAlmostEqual(duration, expected_beat_duration, delta=timing_tolerance)

    def test_playback_timing_change_bpm(self):
        print 'this playback timing test takes ~', TIME_FOR_ASYNC_TESTS, 'seconds'
        timing_tolerance = 0.1
        first_bpm = 240.0
        second_bpm = first_bpm/2.0
        model = Model(8, 8, first_bpm, 0.0, 1)
        first_beat_duration = model._calculate_beat_duration()
        second_beat_duration = first_beat_duration * 2.0
        step_times = []
        def assertion_callback(value):
            step_times.append((time.time(), model._calculate_beat_duration()))

        model.current_beat.add_callback(assertion_callback)
        model.toggle_playback()
        time.sleep(TIME_FOR_ASYNC_TESTS/2.0)
        model.set_bpm(second_bpm)
        time.sleep(TIME_FOR_ASYNC_TESTS/2.0)
        model.toggle_playback()

        for i in range(len(step_times) - 1):
            former, expected_duration = step_times[i]
            latter, _ = step_times[i + 1]
            duration = latter - former
            self.assertAlmostEqual(duration, expected_duration, delta=timing_tolerance)

    def test_playback_timing_swing(self):
        print 'this playback timing test takes ~', TIME_FOR_ASYNC_TESTS, 'seconds'
        timing_tolerance = 0.1
        bpm = 240.0
        swing = .5
        model = Model(8, 8, bpm, swing, 1)
        avg_beat_duration = model._calculate_beat_duration()
        swing_delta = avg_beat_duration * swing/3.0
        step_times = []
        def assertion_callback(value):
            step_times.append((time.time(), value))

        model.current_beat.add_callback(assertion_callback)
        model.toggle_playback()
        time.sleep(TIME_FOR_ASYNC_TESTS)
        model.toggle_playback()

        for i in range(len(step_times) - 1):
            former, beat_number = step_times[i]
            latter, _ = step_times[i + 1]
            duration = latter - former
            expected_beat_duration = avg_beat_duration
            if beat_number % 2 == 0:
                expected_beat_duration = expected_beat_duration + swing_delta
            else:
                expected_beat_duration = expected_beat_duration - swing_delta
            self.assertAlmostEqual(duration, expected_beat_duration, delta=timing_tolerance)


    def test_set_swing(self):
        swing = .5
        model = Model(8, 8, 120.0, swing, 1)
        model.set_swing(1.1)
        self.assertAlmostEqual(model.swing, 1.0, delta=.01)

        model.set_swing(-1.1)
        self.assertAlmostEqual(model.swing, -1.0, delta=.01)

        model.set_swing(-.5)
        self.assertAlmostEqual(model.swing, -.5, delta=.01)

    def test_calculate_beat_duration_no_swing(self):
        timing_tolerance = 1.0
        swing = 0.0
        bpm = 60.0
        model = Model(8, 8, bpm, swing, 1)
        expected_beat_duration = 1.0
        beat_duration = model._calculate_beat_duration()
        self.assertAlmostEqual(expected_beat_duration, beat_duration, delta=timing_tolerance)
        model.current_beat.set_value(1)
        beat_duration = model._calculate_beat_duration()
        self.assertAlmostEqual(expected_beat_duration, beat_duration, delta=timing_tolerance)

    def test_calculate_beat_duration_positive_swing(self):
        timing_tolerance = 0.01
        swing = 1.0
        bpm = 60.0
        model = Model(8, 8, bpm, swing, 1)
        expected_beat_duration_downbeat = 1.0 + swing/3.0
        expected_beat_duration_upbeat = 1.0 - swing/3.0

        downbeat_duration = model._calculate_beat_duration()
        model.current_beat.set_value(1)
        upbeat_duration = model._calculate_beat_duration()
        self.assertAlmostEqual(expected_beat_duration_downbeat, downbeat_duration, delta=timing_tolerance)
        self.assertAlmostEqual(expected_beat_duration_upbeat, upbeat_duration, delta=timing_tolerance)

    def test_calculate_beat_duration_negative_swing(self):
        timing_tolerance = 0.01
        swing = -1.0
        bpm = 60.0
        model = Model(8, 8, bpm, swing, 1)
        expected_beat_duration_downbeat = 1.0 + swing/3.0
        expected_beat_duration_upbeat = 1.0 - swing/3.0

        downbeat_duration = model._calculate_beat_duration()
        model.current_beat.set_value(1)
        upbeat_duration = model._calculate_beat_duration()
        self.assertAlmostEqual(expected_beat_duration_downbeat, downbeat_duration, delta=timing_tolerance)
        self.assertAlmostEqual(expected_beat_duration_upbeat, upbeat_duration, delta=timing_tolerance)

    def test_multiple_columns_per_beat(self):
        print 'this playback timing test takes ~', TIME_FOR_ASYNC_TESTS, 'seconds'
        timing_tolerance = 0.1
        bpm = 240.0
        columns_per_beat = 2
        model = Model(8, 8, bpm, 0.0, columns_per_beat)
        expected_column_duration = model._calculate_beat_duration() / columns_per_beat
        step_times = []
        def assertion_callback(value):
            step_times.append(time.time())

        model.current_beat.add_callback(assertion_callback)
        new_state = model.toggle_playback()
        self.assertTrue(new_state)
        time.sleep(TIME_FOR_ASYNC_TESTS)
        new_state = model.toggle_playback()
        self.assertFalse(new_state)

        for i in range(len(step_times) - 1):
            former = step_times[i]
            latter = step_times[i + 1]
            duration = latter - former
            self.assertAlmostEqual(duration, expected_column_duration, delta=timing_tolerance)

if __name__ == '__main__':
    unittest.main()