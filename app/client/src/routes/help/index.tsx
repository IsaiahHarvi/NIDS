import { createFileRoute } from "@tanstack/react-router";
import { Button } from "@/components/ui/button";

export const Route = createFileRoute("/help/")({
  component: () => (
    <div className="p-8 max-w-3xl mx-auto font-sans">
      <h1 className="text-4xl font-bold mb-4">SecureNet Help Page</h1>
      <h2 className="text-2xl font-semibold mb-6">Welcome to SecureNet</h2>
      <p className="text-lg mb-8">
        SecureNet is a real-time{" "}
        <strong>Network Intrusion Detection System (NIDS)</strong> designed to
        monitor and analyze network traffic, ensuring the security of your
        network infrastructure.
      </p>

      <h3 className="text-xl font-semibold mb-4">About SecureNet</h3>
      <p className="mb-6">
        SecureNet leverages advanced machine learning algorithms to identify
        abnormal patterns in network traffic. By continuously monitoring network
        activities, SecureNet can detect potential threats in real-time, such as
        unauthorized access, data exfiltration, or Distributed Denial of Service
        (DDoS) attacks.
      </p>
      <p className="mb-8">
        The system is designed with cybersecurity best practices in mind,
        providing a robust detection mechanism to safeguard your network.
        SecureNet ensures secure data transmission and promptly alerts
        administrators to any suspicious activities.
      </p>

      <h3 className="text-xl font-semibold mb-4">Why Use SecureNet?</h3>
      <ul className="list-disc list-inside mb-8">
        <li>
          Real-time detection of network intrusions and suspicious activities.
        </li>
        <li>
          Machine learning-powered analysis for accurate threat identification.
        </li>
        <li>
          Customizable alerts for immediate response to potential threats.
        </li>
        <li>
          Adheres to cybersecurity best practices to ensure secure data
          handling.
        </li>
        <li>
          Scalable solution that can be adapted to various network environments.
        </li>
      </ul>

      <h3 className="text-xl font-semibold mb-4">Getting Started</h3>
      <p className="mb-8">
        To get started with SecureNet, navigate to the documentation section
        where you can find setup instructions, configuration options, and best
        practices for deploying SecureNet in your environment.
      </p>

      <Button
        className="py-2 px-4 rounded hover:bg-gray-200 transition duration-200"
        onClick={() =>
          window.open("https://github.com/IsaiahHarvi/NIDS", "_blank")
        }
      >
        Go to Documentation
      </Button>
    </div>
  ),
});
