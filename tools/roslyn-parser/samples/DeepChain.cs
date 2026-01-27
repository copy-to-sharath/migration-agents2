// Synthetic sample to produce a Roslyn graph depth > 10.
// Call chain: Entry -> Step1 -> ... -> Step11 -> Exit
namespace RoslynSample
{
    public class DeepChain
    {
        public void Entry()
        {
            Step1();
        }

        private void Step1() { Step2(); }
        private void Step2() { Step3(); }
        private void Step3() { Step4(); }
        private void Step4() { Step5(); }
        private void Step5() { Step6(); }
        private void Step6() { Step7(); }
        private void Step7() { Step8(); }
        private void Step8() { Step9(); }
        private void Step9() { Step10(); }
        private void Step10() { Step11(); }
        private void Step11() { ExitPoint(); }

        private void ExitPoint()
        {
            // terminal node
        }
    }
}
