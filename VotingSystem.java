package labs.labs9;

import javax.swing.*;
import javax.swing.border.TitledBorder;
import java.awt.*;
import java.text.DecimalFormat;

public class VotingSystem {

    private static JFrame mainFrame;
    private static JPanel resultsPanel;
    private static JPanel propositionsPanel;
    private static JTextArea notesArea;
    private static JLabel donationLabel;
    private static double totalDonations = 0.0;
    private static int candidateAVotes = 0;
    private static int candidateBVotes = 0;
    private static int[] yesVotes;
    private static int[] noVotes;

    public static void main(String[] args) {
        SwingUtilities.invokeLater(VotingSystem::setupElectionDialog);
    }

    private static void setupElectionDialog() {
        while (true) {
            JTextField electionName = new JTextField();
            JTextField candidateA = new JTextField();
            JTextField candidateB = new JTextField();
            JComboBox<Integer> numPropositions = new JComboBox<>();
            for (int i = 1; i <= 15; i++) numPropositions.addItem(i);

            JPanel panel = new JPanel(new GridLayout(5, 2, 5, 5));
            panel.add(new JLabel("Election Name:"));
            panel.add(electionName);
            panel.add(new JLabel("Candidate A Name:"));
            panel.add(candidateA);
            panel.add(new JLabel("Candidate B Name:"));
            panel.add(candidateB);
            panel.add(new JLabel("Num propositions:"));
            panel.add(numPropositions);

            int result = JOptionPane.showConfirmDialog(null, panel, "Election Info",
                    JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);

            if (result == JOptionPane.OK_OPTION) {
                if (electionName.getText().isBlank() || candidateA.getText().isBlank() || candidateB.getText().isBlank()) {
                    JOptionPane.showMessageDialog(null, "All fields must be filled in!");
                } else {
                    int propositionsCount = (int) numPropositions.getSelectedItem();
                    yesVotes = new int[propositionsCount];
                    noVotes = new int[propositionsCount];
                    setupMainScreen(electionName.getText(), candidateA.getText(),
                            candidateB.getText(), propositionsCount);
                    break;
                }
            } else {
                System.exit(0);
            }
        }
    }

    private static void setupMainScreen(String electionName, String candidateA, String candidateB, int numPropositions) {
        mainFrame = new JFrame("Voting System - Mihika Guntur - 75367376");
        mainFrame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        mainFrame.setLayout(new BorderLayout());

        // Add Menu Bar
        JMenuBar menuBar = new JMenuBar();
        JMenu fileMenu = new JMenu("File");
        JMenuItem exitItem = new JMenuItem("Exit");
        exitItem.addActionListener(e -> System.exit(0));
        fileMenu.add(exitItem);
        menuBar.add(fileMenu);
        mainFrame.setJMenuBar(menuBar);

        // Main Content Panel
        JPanel mainContentPanel = new JPanel(new GridBagLayout());
        GridBagConstraints gbc = new GridBagConstraints();
        mainContentPanel.setBorder(BorderFactory.createEmptyBorder(10, 20, 10, 20));

        // Election Title
        JLabel electionTitleLabel = new JLabel(electionName, JLabel.CENTER);
        electionTitleLabel.setFont(new Font("Serif", Font.BOLD, 24));
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        gbc.insets = new Insets(10, 0, 20, 0);
        gbc.anchor = GridBagConstraints.CENTER;
        mainContentPanel.add(electionTitleLabel, gbc);

        // Results Panel
        resultsPanel = new JPanel();
        resultsPanel.setLayout(new BoxLayout(resultsPanel, BoxLayout.Y_AXIS));
        resultsPanel.setBorder(new TitledBorder("Candidates"));
        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.gridwidth = 1;
        gbc.insets = new Insets(10, 10, 10, 10);
        gbc.fill = GridBagConstraints.BOTH;
        mainContentPanel.add(resultsPanel, gbc);

        // Propositions Panel
        propositionsPanel = new JPanel();
        propositionsPanel.setLayout(new BoxLayout(propositionsPanel, BoxLayout.Y_AXIS));
        propositionsPanel.setBorder(new TitledBorder("Propositions"));
        gbc.gridx = 1;
        gbc.gridy = 1;
        mainContentPanel.add(propositionsPanel, gbc);

        // Donation Label
        donationLabel = new JLabel("<html><b>Donation total:</b> " + formatCurrency(totalDonations) + "</html>");
        donationLabel.setFont(new Font("Serif", Font.PLAIN, 14));
        gbc.gridx = 0;
        gbc.gridy = 2;
        gbc.gridwidth = 2;
        gbc.insets = new Insets(10, 0, 10, 0);
        mainContentPanel.add(donationLabel, gbc);

        // Notes Section
        notesArea = new JTextArea(5, 40);
        notesArea.setLineWrap(true);
        notesArea.setWrapStyleWord(true);
        notesArea.setBorder(new TitledBorder("Notes"));
        JScrollPane notesScrollPane = new JScrollPane(notesArea);
        gbc.gridx = 0;
        gbc.gridy = 3;
        gbc.gridwidth = 2;
        gbc.fill = GridBagConstraints.BOTH;
        gbc.insets = new Insets(10, 0, 10, 0);
        mainContentPanel.add(notesScrollPane, gbc);

        // Cast Vote Button
        JButton castVoteButton = new JButton("Cast Vote");
        castVoteButton.setFont(new Font("Serif", Font.BOLD, 14));
        castVoteButton.addActionListener(e -> castVoteDialog(candidateA, candidateB, numPropositions));
        gbc.gridx = 0;
        gbc.gridy = 4;
        gbc.gridwidth = 2;
        gbc.insets = new Insets(20, 0, 10, 0);
        mainContentPanel.add(castVoteButton, gbc);

        mainFrame.add(mainContentPanel, BorderLayout.CENTER);

        updateResults(candidateA, candidateB, numPropositions);

        mainFrame.pack();
        mainFrame.setLocationRelativeTo(null);
        mainFrame.setVisible(true);
    }

    private static void updateResults(String candidateA, String candidateB, int numPropositions) {
        resultsPanel.removeAll();
        propositionsPanel.removeAll();

        Font boldFont = new Font("Default", Font.BOLD, 14);
        Font normalFont = new Font("Default", Font.PLAIN, 12);

        JLabel candidateALabel = new JLabel(candidateA + ": " + candidateAVotes + " votes");
        JLabel candidateBLabel = new JLabel(candidateB + ": " + candidateBVotes + " votes");

        candidateALabel.setFont(candidateAVotes > candidateBVotes ? boldFont : normalFont);
        candidateBLabel.setFont(candidateBVotes > candidateAVotes ? boldFont : normalFont);

        resultsPanel.add(candidateALabel);
        resultsPanel.add(candidateBLabel);

        for (int i = 0; i < numPropositions; i++) {
            JLabel propositionLabel = new JLabel("Prop " + (i + 1) + ": YES: " + yesVotes[i] + " votes, NO: " + noVotes[i] + " votes");
            propositionLabel.setFont(yesVotes[i] > noVotes[i] ? boldFont : normalFont);
            propositionsPanel.add(propositionLabel);
        }

        donationLabel.setText("<html><b>Donation total:</b> " + formatCurrency(totalDonations) + "</html>");

        resultsPanel.revalidate();
        resultsPanel.repaint();
        propositionsPanel.revalidate();
        propositionsPanel.repaint();
    }

    private static void castVoteDialog(String candidateA, String candidateB, int numPropositions) {
        JPanel panel = new JPanel(new BorderLayout(10, 10));

        // Candidates Panel
        JPanel candidatesPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        ButtonGroup candidateGroup = new ButtonGroup();
        JRadioButton voteA = new JRadioButton(candidateA);
        JRadioButton voteB = new JRadioButton(candidateB);
        candidateGroup.add(voteA);
        candidateGroup.add(voteB);
        candidatesPanel.setBorder(new TitledBorder("Candidates"));
        candidatesPanel.add(voteA);
        candidatesPanel.add(voteB);

        // Propositions Panel
        JPanel propositionsPanel = new JPanel(new GridLayout(numPropositions, 3, 5, 5));
        propositionsPanel.setBorder(new TitledBorder("Propositions"));
        JRadioButton[] yesButtons = new JRadioButton[numPropositions];
        JRadioButton[] noButtons = new JRadioButton[numPropositions];
        for (int i = 0; i < numPropositions; i++) {
            JLabel propLabel = new JLabel("Prop " + (i + 1) + ": ");
            JRadioButton yesBox = new JRadioButton("YES");
            JRadioButton noBox = new JRadioButton("NO");
            ButtonGroup propGroup = new ButtonGroup();
            propGroup.add(yesBox);
            propGroup.add(noBox);
            yesButtons[i] = yesBox;
            noButtons[i] = noBox;
            propositionsPanel.add(propLabel);
            propositionsPanel.add(yesBox);
            propositionsPanel.add(noBox);
        }

        // Donation Panel
        JPanel donationPanel = new JPanel(new FlowLayout(FlowLayout.LEFT));
        JCheckBox donationBox = new JCheckBox("I would like to make a donation");
        JTextField donationField = new JTextField("0.00", 10);
        donationField.setEnabled(false);
        donationBox.addActionListener(e -> {
            donationField.setEnabled(donationBox.isSelected());
            if (!donationBox.isSelected()) donationField.setText("0.00");
        });
        donationPanel.setBorder(new TitledBorder("Donation"));
        donationPanel.add(donationBox);
        donationPanel.add(donationField);

        panel.add(candidatesPanel, BorderLayout.NORTH);
        panel.add(propositionsPanel, BorderLayout.CENTER);
        panel.add(donationPanel, BorderLayout.SOUTH);

        int result = JOptionPane.showConfirmDialog(null, panel, "Cast Vote",
                JOptionPane.OK_CANCEL_OPTION, JOptionPane.PLAIN_MESSAGE);

        if (result == JOptionPane.OK_OPTION) {
            try {
                if (voteA.isSelected()) candidateAVotes++;
                if (voteB.isSelected()) candidateBVotes++;
                for (int i = 0; i < numPropositions; i++) {
                    if (yesButtons[i].isSelected()) yesVotes[i]++;
                    if (noButtons[i].isSelected()) noVotes[i]++;
                }
                double donationAmount = Double.parseDouble(donationField.getText());
                if (donationAmount < 0) throw new NumberFormatException();
                totalDonations += donationAmount;
                updateResults(candidateA, candidateB, numPropositions);
            } catch (NumberFormatException ex) {
                JOptionPane.showMessageDialog(null, "Please enter a valid donation amount.");
                castVoteDialog(candidateA, candidateB, numPropositions);
            }
        }
    }

    private static String formatCurrency(double amount) {
        DecimalFormat df = new DecimalFormat("$#,##0.00");
        return df.format(amount);
    }


 // MAIN FUNCTION 
 public class Main {
    public static void main(String[] args) {
        Main.main(args);
    }
}
}